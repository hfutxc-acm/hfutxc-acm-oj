from datetime import datetime
from pathlib import Path
import asyncio
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

from fastapi import BackgroundTasks, Body, Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import inspect, text, update
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

try:
    from .database import Base, PROJECT_ROOT, SessionLocal, engine, get_db
    from .models import Problem, Submission, SubmissionResult, TestCase, User, Group
except ImportError:
    from database import PROJECT_ROOT, async_session_maker, engine, get_db, init_db
    from models import Problem, Submission, SubmissionResult, TestCase, User, Group

from auth import get_password_hash, verify_password, create_access_token, decode_access_token

from routers import auth as auth_router
from routers import users as users_router
from routers import groups as groups_router
from routers import admin as admin_router
from services.judge_worker import judge_queue, judge_worker_loop
from admin_panel import init_admin

DATA_ROOT = PROJECT_ROOT / "data" / "problems"
CASE_FILE_RE = re.compile(r"^([1-9]\d*)\.(in|out)$")
FORBIDDEN_SUFFIXES = {".exe", ".py", ".bat", ".sh", ".cmd", ".ps1"}

JUDGE0_API_URL = os.environ.get("JUDGE0_API_URL", "https://judge0-ce.p.rapidapi.com")
JUDGE0_API_KEY = os.environ.get("JUDGE0_API_KEY", "")

JUDGE0_LANG_MAP = {
    "cpp": 54, "c++": 54, "c++17": 54,
    "c": 50,
    "python": 71, "py": 71, "python3": 71,
    "java": 62,
    "go": 60,
    "rust": 73,
    "javascript": 63, "js": 63,
    "csharp": 51, "c#": 51,
    "kotlin": 78
}


DATA_ROOT.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = PROJECT_ROOT / "uploads"
AVATAR_DIR = UPLOAD_DIR / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="HFUTXC ACM OJ API", version="1.3.0")

app.add_middleware(SessionMiddleware, secret_key="oj-super-secret-key-for-admin")

@app.on_event("startup")
async def startup_event():
    await init_db()
    asyncio.create_task(judge_worker_loop())
    init_admin(app, engine)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(groups_router.router)
app.include_router(admin_router.router)
from routers import printer as printer_router
from routers import ai as ai_router
app.include_router(printer_router.router)
app.include_router(ai_router.router)
app.mount("/api/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

wiki_site_path = PROJECT_ROOT / "wiki" / "site"
if wiki_site_path.exists():
    app.mount("/wiki", StaticFiles(directory=str(wiki_site_path), html=True), name="wiki")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProblemPayload(BaseModel):
    title: str = Field(min_length=1)
    difficulty: str | int = "Easy"
    description: str = ""
    input_description: str | None = None
    output_description: str | None = None
    time_limit_ms: int | float = Field(default=1000, ge=100, le=60000)
    memory_limit_mb: int | float = Field(default=256, ge=16, le=4096)
    is_public: bool = True


class SubmitCodeRequest(BaseModel):
    user_id: int
    problem_id: int
    language: str
    code: str


class DeleteProblemConfirm(BaseModel):
    confirm_problem_id: int


def testcase_count(problem: Problem) -> int:
    return len(problem.testcases or [])


def serialize_problem(problem: Problem):
    return {
        "id": problem.id,
        "title": problem.title,
        "difficulty": problem.difficulty,
        "description": problem.description,
        "input_description": problem.input_description,
        "output_description": problem.output_description,
        "time_limit_ms": problem.time_limit_ms,
        "memory_limit_mb": problem.memory_limit_mb,
        "is_public": problem.is_public,
        "created_at": problem.created_at,
        "updated_at": problem.updated_at,
        "testcase_count": testcase_count(problem),
    }


def serialize_testcase(case: TestCase):
    return {
        "id": case.id,
        "problem_id": case.problem_id,
        "input_path": case.input_path,
        "output_path": case.output_path,
        "score": case.score,
        "sort_order": case.sort_order,
        "is_sample": case.is_sample,
        "created_at": case.created_at,
    }


def apply_problem_payload(problem: Problem, payload: ProblemPayload):
    problem.title = payload.title.strip()
    problem.difficulty = payload.difficulty
    problem.description = payload.description
    problem.input_description = payload.input_description
    problem.output_description = payload.output_description
    problem.time_limit_ms = payload.time_limit_ms
    problem.memory_limit_mb = payload.memory_limit_mb
    problem.is_public = payload.is_public
    problem.updated_at = datetime.utcnow()


def validate_zip_members(upload_path: Path):
    inputs: dict[int, zipfile.ZipInfo] = {}
    outputs: dict[int, zipfile.ZipInfo] = {}

    try:
        archive = zipfile.ZipFile(upload_path)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="不是有效的 zip 文件")

    with archive:
        for info in archive.infolist():
            name = info.filename
            pure_name = Path(name).name
            if info.is_dir():
                raise HTTPException(status_code=400, detail=f"zip 不支持目录: {name}")
            if not name or name != pure_name or "/" in name or "\\" in name or ".." in Path(name).parts:
                raise HTTPException(status_code=400, detail=f"非法文件路径: {name}")
            if not name.isascii():
                raise HTTPException(status_code=400, detail=f"文件名必须为 ASCII: {name}")
            if Path(name).suffix.lower() in FORBIDDEN_SUFFIXES:
                raise HTTPException(status_code=400, detail=f"禁止上传文件类型: {name}")

            match = CASE_FILE_RE.fullmatch(name)
            if not match:
                raise HTTPException(status_code=400, detail=f"测试点文件名必须是 数字.in 或 数字.out: {name}")

            order = int(match.group(1))
            kind = match.group(2)
            target = inputs if kind == "in" else outputs
            if order in target:
                raise HTTPException(status_code=400, detail=f"重复测试点文件: {name}")
            target[order] = info

        input_orders = set(inputs)
        output_orders = set(outputs)
        if not input_orders and not output_orders:
            raise HTTPException(status_code=400, detail="zip 中至少需要一个测试点")
        missing_out = sorted(input_orders - output_orders)
        missing_in = sorted(output_orders - input_orders)
        if missing_out:
            raise HTTPException(status_code=400, detail=f"缺少对应 .out 文件: {missing_out}")
        if missing_in:
            raise HTTPException(status_code=400, detail=f"缺少对应 .in 文件: {missing_in}")

    return sorted(input_orders)


async def replace_problem_data(problem_id: int, upload_path: Path, orders: list[int], db: AsyncSession):
    problem_dir = (DATA_ROOT / str(problem_id)).resolve()
    data_root = DATA_ROOT.resolve()
    if problem_dir.parent != data_root:
        raise HTTPException(status_code=400, detail="非法题目数据目录")

    if problem_dir.exists():
        shutil.rmtree(problem_dir)
    problem_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(upload_path) as archive:
        for order in orders:
            for suffix in ("in", "out"):
                name = f"{order}.{suffix}"
                dest = (problem_dir / name).resolve()
                if dest.parent != problem_dir:
                    raise HTTPException(status_code=400, detail=f"非法解压路径: {name}")
                with archive.open(name) as src, dest.open("wb") as out:
                    shutil.copyfileobj(src, out)

    # deleted via sqlmodel
    from sqlalchemy import delete as sa_delete
    await db.exec(sa_delete(TestCase).where(TestCase.problem_id == problem_id))
    for order in orders:
        db.add(
            TestCase(
                problem_id=problem_id,
                input_path=str((problem_dir / f"{order}.in").relative_to(PROJECT_ROOT)).replace("\\", "/"),
                output_path=str((problem_dir / f"{order}.out").relative_to(PROJECT_ROOT)).replace("\\", "/"),
                score=10,
                sort_order=order,
                is_sample=False,
            )
        )
    await db.commit()


@app.get("/api/problems")
async def get_problem_list(db: AsyncSession = Depends(get_db)):
    return [serialize_problem(problem) for problem in (await db.exec(select(Problem).order_by(Problem.id.asc()))).all()]


@app.get("/api/problems/{problem_id}")
async def get_problem_detail(problem_id: int, db: AsyncSession = Depends(get_db)):
    problem = (await db.exec(select(Problem).where(Problem.id == problem_id))).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    return serialize_problem(problem)


@app.post("/api/admin/problems")
async def create_problem(
    payload: ProblemPayload | None = Body(default=None),
    title: str | None = Query(default=None),
    difficulty: str = Query(default="Easy"),
    description: str = Query(default="这是默认题面描述"),
    db: AsyncSession = Depends(get_db),
):
    if payload is None:
        if not title:
            raise HTTPException(status_code=400, detail="请提供题目标题")
        payload = ProblemPayload(title=title, difficulty=difficulty, description=description)
    problem = Problem()
    apply_problem_payload(problem, payload)
    problem.created_at = datetime.utcnow()
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    return {"id": problem.id, "message": "problem created"}


@app.put("/api/admin/problems/{problem_id}")
async def update_problem(problem_id: int, payload: ProblemPayload, db: AsyncSession = Depends(get_db)):
    problem = (await db.exec(select(Problem).where(Problem.id == problem_id))).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    apply_problem_payload(problem, payload)
    await db.commit()
    await db.refresh(problem)
    return serialize_problem(problem)


@app.delete("/api/admin/problems/{problem_id}")
async def delete_problem(
    problem_id: int,
    confirm: DeleteProblemConfirm = Body(...),
    db: AsyncSession = Depends(get_db),
):
    if confirm.confirm_problem_id != problem_id:
        raise HTTPException(status_code=400, detail="确认题号不匹配，已取消删除")

    problem = (await db.exec(select(Problem).where(Problem.id == problem_id))).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")

    try:
        submission_ids = [
            row
            for row in (await db.exec(select(Submission.id).where(Submission.problem_id == problem_id))).all()
        ]
        testcase_ids = [
            row
            for row in (await db.exec(select(TestCase.id).where(TestCase.problem_id == problem_id))).all()
        ]

        from sqlalchemy import delete as sa_delete

        if submission_ids:
            await db.exec(sa_delete(SubmissionResult).where(
                SubmissionResult.submission_id.in_(submission_ids)
            ))
        if testcase_ids:
            await db.exec(sa_delete(SubmissionResult).where(
                SubmissionResult.testcase_id.in_(testcase_ids)
            ))

        await db.exec(sa_delete(Submission).where(
            Submission.problem_id == problem_id
        ))
        await db.exec(sa_delete(TestCase).where(
            TestCase.problem_id == problem_id
        ))

        problem_dir = (DATA_ROOT / str(problem_id)).resolve()
        if problem_dir.exists():
            data_root = DATA_ROOT.resolve()
            if problem_dir.parent != data_root:
                raise HTTPException(status_code=400, detail="非法题目数据目录")
            shutil.rmtree(problem_dir)

        db.delete(problem)
        await db.commit()
        return {"message": "Problem deleted successfully", "problem_id": problem_id}
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(exc)}")


@app.post("/api/admin/problems/{problem_id}/testcases/upload")
async def upload_testcases(problem_id: int, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    problem = (await db.exec(select(Problem).where(Problem.id == problem_id))).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    if not file.filename or not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="请上传 zip 文件")

    with tempfile.TemporaryDirectory(prefix="oj-upload-") as tmp:
        upload_path = Path(tmp) / "problem_data.zip"
        with upload_path.open("wb") as out:
            shutil.copyfileobj(file.file, out)
        orders = validate_zip_members(upload_path)
        replace_problem_data(problem_id, upload_path, orders, db)

    return {"message": "uploaded", "problem_id": problem_id, "case_count": len(orders)}


@app.get("/api/admin/problems/{problem_id}/testcases")
async def get_problem_testcases(problem_id: int, db: AsyncSession = Depends(get_db)):
    problem = (await db.exec(select(Problem).where(Problem.id == problem_id))).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    cases = (await db.exec(select(TestCase).where(TestCase.problem_id == problem_id).order_by(TestCase.sort_order.asc()))).all()
    return [serialize_testcase(case) for case in cases]




@app.post("/api/submit")
async def submit_code(req: SubmitCodeRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    problem = (await db.exec(select(Problem).where(Problem.id == req.problem_id))).first()
    user = (await db.exec(select(User).where(User.id == req.user_id))).first()
    if not problem or not user:
        raise HTTPException(status_code=400, detail="用户或题目不存在，无法提交记录")

    new_submission = Submission(
        user_id=req.user_id,
        problem_id=req.problem_id,
        language=req.language,
        code=req.code,
        status="Pending",
    )
    db.add(new_submission)
    await db.commit()
    db.refresh(new_submission)

    from services.judge_worker import judge_queue
    await judge_queue.put(new_submission.id)

    return {
        "message": "代码提交成功，已进入评测队列",
        "submission_id": new_submission.id,
        "current_status": "Pending",
    }


@app.get("/api/submissions/{submission_id}")
async def get_submission_status(submission_id: int, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Submission, User.username, Problem.title)
        .outerjoin(User, Submission.user_id == User.id)
        .outerjoin(Problem, Submission.problem_id == Problem.id)
        .where(Submission.id == submission_id)
    )
    row = (await db.exec(stmt)).first()
    if not row:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    submission, username, problem_title = row
    results = (await db.exec(select(SubmissionResult).where(SubmissionResult.submission_id == submission_id))).all()
    return {
        "id": submission.id,
        "status": submission.status,
        "language": submission.language,
        "code": submission.code,
        "user_id": submission.user_id,
        "username": username or f"User #{submission.user_id}",
        "problem_id": submission.problem_id,
        "problem_title": problem_title or f"Problem #{submission.problem_id}",
        "time_ms": submission.time_ms,
        "memory_kb": submission.memory_kb,
        "created_at": submission.created_at.isoformat() if submission.created_at else None,
        "results": [
            {
                "testcase_id": r.testcase_id,
                "status": r.status,
                "message": r.message,
                "time_ms": r.time_ms,
                "memory_kb": r.memory_kb
            } for r in results
        ]
    }


@app.get("/api/submissions")
async def get_all_submissions(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Submission, User.username, Problem.title)
        .outerjoin(User, Submission.user_id == User.id)
        .outerjoin(Problem, Submission.problem_id == Problem.id)
        .order_by(Submission.id.desc())
        .limit(50)
    )
    rows = (await db.exec(stmt)).all()
    return [
        {
            "id": sub.id,
            "user_id": sub.user_id,
            "username": username or f"User #{sub.user_id}",
            "problem_id": sub.problem_id,
            "problem_title": title or f"Problem #{sub.problem_id}",
            "language": sub.language,
            "status": sub.status,
            "time_ms": sub.time_ms,
            "memory_kb": sub.memory_kb,
            "created_at": sub.created_at.isoformat() if sub.created_at else None,
        }
        for sub, username, title in rows
    ]
