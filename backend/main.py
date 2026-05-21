from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio

from database import engine, Base, get_db
from models import Problem, User, Submission

# 启动时自动扫描并创建所有新表（users 和 submissions）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HFUTXC ACM OJ API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic 核心模型：用于接收前端传来的 JSON
class SubmitCodeRequest(BaseModel):
    user_id: int  # 新增：告诉后端是谁提交的
    problem_id: int
    language: str
    code: str


# 异步评测核心工作流占位
async def run_judger_worker(submission_id: int, db_session_factory, code: str, lang: str):
    """
    异步评测任务。由于要在后台线程更新数据库，
    我们传入 db_session_factory 用来在需要时创建独立的数据库连接。
    """
    print(f"[评测机] 收到提交记录 #{submission_id}，启动评测流...")

    # 模拟评测机编译运行需要 3 秒
    await asyncio.sleep(3)

    # 评测完成后，我们要把结果同步更新到刚才建的数据库表里
    db = db_session_factory()
    try:
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if submission:
            submission.status = "AC"  # 模拟评测通过，真实情况这里由 C++ 评测机决定
            db.commit()
            print(f"[评测机] 提交记录 #{submission_id} 状态已更新为: AC")
    finally:
        db.close()


# ==========================================
# 路由接口开发
# ==========================================

@app.get("/api/problems")
async def get_problem_list(db: Session = Depends(get_db)):
    return db.query(Problem).all()


@app.post("/api/admin/problems")
async def create_problem(title: str, difficulty: str, description: str = "这是默认题面描述", db: Session = Depends(get_db)):
    new_problem = Problem(title=title, difficulty=difficulty, description=description) # 👈 加上 description
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem


# --- 新增接口：快捷创建测试用户 ---
@app.post("/api/admin/users")
async def create_user(username: str, db: Session = Depends(get_db)):
    # 先写死一个简易的哈希占位密码
    new_user = User(username=username, hashed_password="mock_hashed_password")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "用户创建成功", "user": new_user}


# --- 重构核心业务：提交代码并生成真实记录 ---
@app.post("/api/submit")
async def submit_code(req: SubmitCodeRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. 严格检查：提交的题目和用户是否存在，如果不存在直接拦截，防止外键冲突
    problem = db.query(Problem).filter(Problem.id == req.problem_id).first()
    user = db.query(User).filter(User.id == req.user_id).first()
    if not problem or not user:
        raise HTTPException(status_code=400, detail="用户或题目不存在，无法提交记录")

    # 2. 在 submissions 表中新建一条真实的 Pending 记录
    new_submission = Submission(
        user_id=req.user_id,
        problem_id=req.problem_id,
        language=req.language,
        code=req.code,
        status="Pending"  # 一开始的状态是排队中
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)  # 这一步执行完，我们就拿到了自增的真实 submission.id

    # 3. 将这个真实的自增 ID 丢给后台的异步工作线程
    # 注意：我们这里把 SessionLocal 传进去，方便后台任务在未来独立连接数据库
    from database import SessionLocal
    background_tasks.add_task(
        run_judger_worker,
        new_submission.id,
        SessionLocal,
        req.code,
        req.language
    )

    # 4. 立刻向前端交卷
    return {
        "message": "代码提交成功，已进入评测队列",
        "submission_id": new_submission.id,
        "current_status": "Pending"
    }

# --- 新增接口：查询指定提交记录的状态 ---
@app.get("/api/submissions/{submission_id}")
async def get_submission_status(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="提交记录不存在")
    return {
        "id": submission.id,
        "status": submission.status,
        "language": submission.language,
        "created_at": submission.created_at
    }

# --- 新增接口：获取历史提交大厅列表 ---
@app.get("/api/submissions")
async def get_all_submissions(db: Session = Depends(get_db)):
    # 按 ID 倒序（最新提交在最前），最多拉取最新的 20 条
    return db.query(Submission).order_by(Submission.id.desc()).limit(20).all()