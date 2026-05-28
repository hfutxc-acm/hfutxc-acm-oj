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
from fastapi.staticfiles import StaticFiles
import uuid
from pydantic import BaseModel, Field
from sqlalchemy import inspect, text, update
from sqlalchemy.orm import Session

try:
    from .database import Base, PROJECT_ROOT, SessionLocal, engine, get_db
    from .models import Problem, Submission, SubmissionResult, TestCase, User, Group
except ImportError:
    from database import Base, PROJECT_ROOT, SessionLocal, engine, get_db
    from models import Problem, Submission, SubmissionResult, TestCase, User, Group

from auth import get_password_hash, verify_password, create_access_token, decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的或已过期的 Token")
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="未找到用户")
    return user

def check_admin_role(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


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


def ensure_sqlite_columns():
    """MVP 迁移：旧 SQLite 表存在时，补齐新增字段。"""
    inspector = inspect(engine)
    if "problems" not in inspector.get_table_names():
        return

    existing = {col["name"] for col in inspector.get_columns("problems")}
    columns = {
        "input_description": "TEXT",
        "output_description": "TEXT",
        "time_limit_ms": "INTEGER NOT NULL DEFAULT 1000",
        "memory_limit_mb": "INTEGER NOT NULL DEFAULT 256",
        "is_public": "BOOLEAN NOT NULL DEFAULT 1",
        "created_at": "DATETIME",
        "updated_at": "DATETIME",
    }
    with engine.begin() as conn:
        for name, ddl in columns.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE problems ADD COLUMN {name} {ddl}"))
        now = datetime.utcnow()
        conn.execute(update(Problem).where(Problem.created_at == None).values(created_at=now))
        conn.execute(update(Problem).where(Problem.updated_at == None).values(updated_at=now))


Base.metadata.create_all(bind=engine)
ensure_sqlite_columns()
DATA_ROOT.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = PROJECT_ROOT / "uploads"
AVATAR_DIR = UPLOAD_DIR / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="HFUTXC ACM OJ API", version="1.3.0")

app.mount("/api/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

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


def replace_problem_data(problem_id: int, upload_path: Path, orders: list[int], db: Session):
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

    db.query(TestCase).filter(TestCase.problem_id == problem_id).delete()
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
    db.commit()


def judge0_submit(code: str, language: str, stdin_text: str, timeout_s: float):
    import subprocess
    import tempfile
    
    if JUDGE0_API_URL == "local":
        if language.lower() in ["python", "py", "python3"]:
            try:
                res = subprocess.run(["python3", "-c", code], input=stdin_text, text=True, capture_output=True, timeout=timeout_s)
                if res.returncode == 0:
                    return {"status": "OK", "stdout": res.stdout, "message": "", "time_ms": 10}
                else:
                    return {"status": "RE", "stdout": res.stdout, "message": res.stderr, "time_ms": 10}
            except subprocess.TimeoutExpired:
                return {"status": "TLE", "stdout": "", "message": "运行超时", "time_ms": int(timeout_s * 1000)}
            except Exception as e:
                return {"status": "SE", "stdout": "", "message": str(e), "time_ms": 0}
        elif language.lower() in ["cpp", "c++", "c"]:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = Path(tmpdir) / "main.cpp"
                exe = Path(tmpdir) / "a.out"
                src.write_text(code, encoding="utf-8")
                cpp_compiler = os.environ.get("CPP_COMPILER", "g++")
                comp = subprocess.run([cpp_compiler, "-O2", "-std=c++17", str(src), "-o", str(exe)], capture_output=True, text=True)
                if comp.returncode != 0:
                    return {"status": "CE", "stdout": "", "message": comp.stderr, "time_ms": 0}
                try:
                    res = subprocess.run([str(exe)], input=stdin_text, text=True, capture_output=True, timeout=timeout_s)
                    if res.returncode == 0:
                        return {"status": "OK", "stdout": res.stdout, "message": "", "time_ms": 10}
                    else:
                        return {"status": "RE", "stdout": res.stdout, "message": res.stderr, "time_ms": 10}
                except subprocess.TimeoutExpired:
                    return {"status": "TLE", "stdout": "", "message": "运行超时", "time_ms": int(timeout_s * 1000)}
                except Exception as e:
                    return {"status": "SE", "stdout": "", "message": str(e), "time_ms": 0}
        else:
            return {"status": "CE", "stdout": "", "message": f"本地原生模式暂不支持该语言: {language}", "time_ms": 0}

    lang_id = JUDGE0_LANG_MAP.get(language.lower())
    if not lang_id:
        return {"status": "CE", "stdout": "", "message": f"Judge0 暂不支持语言: {language}", "time_ms": 0}

    payload = {
        "source_code": base64.b64encode(code.encode("utf-8")).decode("utf-8"),
        "language_id": lang_id,
        "stdin": base64.b64encode(stdin_text.encode("utf-8")).decode("utf-8"),
        "cpu_time_limit": timeout_s
    }

    headers = {"Content-Type": "application/json"}
    if "rapidapi" in JUDGE0_API_URL:
        host = JUDGE0_API_URL.replace("https://", "").replace("http://", "").split("/")[0]
        headers["x-rapidapi-host"] = host
        if JUDGE0_API_KEY:
            headers["x-rapidapi-key"] = JUDGE0_API_KEY

    try:
        url = f"{JUDGE0_API_URL}/submissions?base64_encoded=true&wait=true"
        resp = requests.post(url, json=payload, headers=headers, timeout=max(timeout_s + 5, 10))
        resp.raise_for_status()
        data = resp.json()

        status_id = data.get("status", {}).get("id", 0)
        time_elapsed = int(float(data.get("time") or 0) * 1000)

        stdout_raw = data.get("stdout")
        stdout = base64.b64decode(stdout_raw).decode("utf-8") if stdout_raw else ""

        compile_output_raw = data.get("compile_output")
        compile_output = base64.b64decode(compile_output_raw).decode("utf-8", errors="replace") if compile_output_raw else ""

        message_raw = data.get("message")
        stderr = base64.b64decode(message_raw).decode("utf-8", errors="replace") if message_raw else ""

        err_msg = compile_output or stderr

        if status_id == 3 or status_id == 4:
            return {"status": "OK", "stdout": stdout, "message": "", "time_ms": time_elapsed}
        elif status_id == 5:
            return {"status": "TLE", "stdout": stdout, "message": "运行超时", "time_ms": time_elapsed}
        elif status_id == 6:
            return {"status": "CE", "stdout": "", "message": err_msg, "time_ms": 0}
        elif 7 <= status_id <= 12:
            return {"status": "RE", "stdout": stdout, "message": err_msg, "time_ms": time_elapsed}
        else:
            return {"status": "SE", "stdout": stdout, "message": f"Judge0 System Error: {status_id} {err_msg}", "time_ms": 0}

    except requests.RequestException as exc:
        return {"status": "SE", "stdout": "", "message": f"API调用失败: {str(exc)}", "time_ms": 0}


async def run_judger_worker(submission_id: int, db_session_factory):
    print(f"[评测机] 收到提交记录 #{submission_id}，启动评测流...")
    await asyncio.sleep(0.1)

    db = db_session_factory()
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            return

        problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
        cases = (
            db.query(TestCase)
            .filter(TestCase.problem_id == submission.problem_id)
            .order_by(TestCase.sort_order.asc())
            .all()
        )
        if not problem or not cases:
            submission.status = "SE"
            db.commit()
            return

        db.query(SubmissionResult).filter(SubmissionResult.submission_id == submission_id).delete()
        final_status = "AC"
        timeout_s = max(0.1, problem.time_limit_ms / 1000)

        for case in cases:
            input_path = PROJECT_ROOT / case.input_path
            output_path = PROJECT_ROOT / case.output_path
            try:
                stdin_text = input_path.read_text(encoding="utf-8")
                expected_output = output_path.read_text(encoding="utf-8")
            except OSError as exc:
                final_status = "SE"
                db.add(SubmissionResult(submission_id=submission_id, testcase_id=case.id, status="SE", message=str(exc)))
                break

            run_result = judge0_submit(submission.code, submission.language, stdin_text, timeout_s)
            status = run_result["status"]
            if status == "OK":
                status = "AC" if run_result["stdout"].rstrip() == expected_output.rstrip() else "WA"

            db.add(
                SubmissionResult(
                    submission_id=submission_id,
                    testcase_id=case.id,
                    status=status,
                    time_ms=run_result.get("time_ms", 0),
                    memory_kb=0,
                    message=run_result.get("message") or "",
                )
            )

            if status != "AC":
                final_status = status
                break

        submission.status = final_status
        db.commit()
        print(f"[评测机] 提交记录 #{submission_id} 状态已更新为: {final_status}")
    finally:
        db.close()


@app.get("/api/problems")
async def get_problem_list(db: Session = Depends(get_db)):
    return [serialize_problem(problem) for problem in db.query(Problem).order_by(Problem.id.asc()).all()]


@app.get("/api/problems/{problem_id}")
async def get_problem_detail(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    return serialize_problem(problem)


@app.post("/api/admin/problems")
async def create_problem(
    payload: ProblemPayload | None = Body(default=None),
    title: str | None = Query(default=None),
    difficulty: str = Query(default="Easy"),
    description: str = Query(default="这是默认题面描述"),
    db: Session = Depends(get_db),
):
    if payload is None:
        if not title:
            raise HTTPException(status_code=400, detail="请提供题目标题")
        payload = ProblemPayload(title=title, difficulty=difficulty, description=description)
    problem = Problem()
    apply_problem_payload(problem, payload)
    problem.created_at = datetime.utcnow()
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return {"id": problem.id, "message": "problem created"}


@app.put("/api/admin/problems/{problem_id}")
async def update_problem(problem_id: int, payload: ProblemPayload, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    apply_problem_payload(problem, payload)
    db.commit()
    db.refresh(problem)
    return serialize_problem(problem)


@app.delete("/api/admin/problems/{problem_id}")
async def delete_problem(
    problem_id: int,
    confirm: DeleteProblemConfirm = Body(...),
    db: Session = Depends(get_db),
):
    if confirm.confirm_problem_id != problem_id:
        raise HTTPException(status_code=400, detail="确认题号不匹配，已取消删除")

    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")

    try:
        submission_ids = [
            row.id
            for row in db.query(Submission.id).filter(Submission.problem_id == problem_id).all()
        ]
        testcase_ids = [
            row.id
            for row in db.query(TestCase.id).filter(TestCase.problem_id == problem_id).all()
        ]

        if submission_ids:
            db.query(SubmissionResult).filter(
                SubmissionResult.submission_id.in_(submission_ids)
            ).delete(synchronize_session=False)
        if testcase_ids:
            db.query(SubmissionResult).filter(
                SubmissionResult.testcase_id.in_(testcase_ids)
            ).delete(synchronize_session=False)

        db.query(Submission).filter(
            Submission.problem_id == problem_id
        ).delete(synchronize_session=False)
        db.query(TestCase).filter(
            TestCase.problem_id == problem_id
        ).delete(synchronize_session=False)

        problem_dir = (DATA_ROOT / str(problem_id)).resolve()
        if problem_dir.exists():
            data_root = DATA_ROOT.resolve()
            if problem_dir.parent != data_root:
                raise HTTPException(status_code=400, detail="非法题目数据目录")
            shutil.rmtree(problem_dir)

        db.delete(problem)
        db.commit()
        return {"message": "Problem deleted successfully", "problem_id": problem_id}
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(exc)}")


@app.post("/api/admin/problems/{problem_id}/testcases/upload")
async def upload_testcases(problem_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
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
async def get_problem_testcases(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    cases = db.query(TestCase).filter(TestCase.problem_id == problem_id).order_by(TestCase.sort_order.asc()).all()
    return [serialize_testcase(case) for case in cases]


from auth import get_password_hash

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/api/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "role": user.role}

@app.get("/api/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
        "avatar_url": current_user.avatar_url
    }

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/api/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="用户名已被注册")
    hashed_pwd = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "用户注册成功", "user_id": new_user.id, "username": new_user.username}

@app.post("/api/users/{user_id}/avatar")
async def upload_avatar(user_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权修改他人头像")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传有效的图片文件")
    
    ext = file.filename.split(".")[-1] if "." in file.filename else "png"
    filename = f"avatar_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = AVATAR_DIR / filename
    
    with filepath.open("wb") as out:
        shutil.copyfileobj(file.file, out)
        
    user.avatar_url = f"/api/uploads/avatars/{filename}"
    db.commit()
    return {"message": "头像上传成功", "avatar_url": user.avatar_url}

class GroupCreate(BaseModel):
    name: str
    description: str = ""

@app.get("/api/groups")
async def get_groups(db: Session = Depends(get_db)):
    groups = db.query(Group).all()
    return [{"id": g.id, "name": g.name, "description": g.description} for g in groups]

@app.post("/api/groups")
async def create_group(group: GroupCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Group).filter(Group.name == group.name).first():
        raise HTTPException(status_code=400, detail="组织名已存在")
    new_group = Group(name=group.name, description=group.description, owner_id=current_user.id)
    db.add(new_group)
    current_user.groups.append(new_group)
    db.commit()
    db.refresh(new_group)
    return {"message": "创建成功", "group": {"id": new_group.id, "name": new_group.name}}

@app.post("/api/groups/{group_id}/join")
async def join_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="组织不存在")
    if group not in current_user.groups:
        current_user.groups.append(group)
        db.commit()
    return {"message": "成功加入组织"}

@app.post("/api/groups/{group_id}/leave")
async def leave_group(group_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="组织不存在")
    if group in current_user.groups:
        current_user.groups.remove(group)
        db.commit()
    return {"message": "成功退出组织"}

@app.get("/api/users/{user_id}")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "groups": [{"id": g.id, "name": g.name} for g in user.groups],
        "submissions_count": len(user.submissions),
        "ac_count": len([s for s in user.submissions if s.status == "OK"])
    }

@app.get("/api/admin/users")
async def get_all_users(current_user: User = Depends(check_admin_role), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{
        "id": u.id,
        "username": u.username,
        "role": u.role,
        "avatar_url": u.avatar_url,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "groups": [{"id": g.id, "name": g.name} for g in u.groups]
    } for u in users]

@app.put("/api/admin/users/{user_id}/role")
async def update_user_role(user_id: int, role: str = Body(embed=True), current_user: User = Depends(check_admin_role), db: Session = Depends(get_db)):
    if role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="无效的角色")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.role = role
    db.commit()
    return {"message": "角色更新成功", "role": user.role}

@app.post("/api/submit")
async def submit_code(req: SubmitCodeRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == req.problem_id).first()
    user = db.query(User).filter(User.id == req.user_id).first()
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
    db.commit()
    db.refresh(new_submission)

    background_tasks.add_task(run_judger_worker, new_submission.id, SessionLocal)

    return {
        "message": "代码提交成功，已进入评测队列",
        "submission_id": new_submission.id,
        "current_status": "Pending",
    }


@app.get("/api/submissions/{submission_id}")
async def get_submission_status(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    results = db.query(SubmissionResult).filter(SubmissionResult.submission_id == submission_id).all()
    return {
        "id": submission.id,
        "status": submission.status,
        "language": submission.language,
        "code": submission.code,
        "user_id": submission.user_id,
        "problem_id": submission.problem_id,
        "created_at": submission.created_at,
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
async def get_all_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).order_by(Submission.id.desc()).limit(20).all()
