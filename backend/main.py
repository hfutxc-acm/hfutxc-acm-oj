from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio

# 引入我们刚刚写的数据库组件
from database import engine, Base, get_db
from models import Problem

# 自动在 SQLite 中创建所有未建立的表（如果 oj.db 不存在，会自动生成）
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HFUTXC ACM OJ API",
    description="在线评测系统后端核心接口（SQLite 驱动版）",
    version="1.1.0"
)

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 模型（用于 API 数据校验）
class SubmitCodeRequest(BaseModel):
    problem_id: int
    language: str
    code: str

# 核心业务：异步评测占位
async def run_judger_worker(submission_id: int, code: str, lang: str):
    print(f"[评测机] 正在编译运行提交 #{submission_id}, 语言: {lang}...")
    await asyncio.sleep(2)
    print(f"[评测机] 提交 #{submission_id} 评测完成！结果: AC")

# ==========================================
# 5. API 路由设计（真正连接数据库）
# ==========================================

@app.get("/")
async def root():
    return {"message": "Hello, OJ 正常运行在 SQLite 驱动下！"}

# --- 1. 获取全站题目列表 ---
@app.get("/api/problems")
async def get_problem_list(db: Session = Depends(get_db)):
    # 这一行就是 SQLAlchemy 的黑魔法，相当于执行了 SELECT * FROM problems;
    problems = db.query(Problem).all()
    return problems

# --- 2. 管理员专用：快捷创建题目（方便我们测试） ---
@app.post("/api/admin/problems")
async def create_problem(title: str, difficulty: str, db: Session = Depends(get_db)):
    # 创建一个题目对象
    new_problem = Problem(title=title, difficulty=difficulty)
    # 塞进数据库并提交
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)  # 刷新以获取自动生成的 id
    return {"message": "题目创建成功", "problem": new_problem}

# --- 3. 获取单道题目详情 ---
@app.get("/api/problems/{problem_id}")
async def get_problem_detail(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="题目不存在")
    return problem

# --- 4. 提交代码 ---
@app.post("/api/submit")
async def submit_code(req: SubmitCodeRequest, background_tasks: BackgroundTasks):
    mock_submission_id = 9527
    background_tasks.add_task(run_judger_worker, mock_submission_id, req.code, req.language)
    return {
        "message": "代码已提交，评测排队中...",
        "submission_id": mock_submission_id,
        "status": "Pending"
    }