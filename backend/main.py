from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio

# ==========================================
# 1. 初始化 FastAPI 应用
# ==========================================
app = FastAPI(
    title="HFUTXC ACM OJ API",
    description="在线评测系统后端核心接口",
    version="1.0.0"
)

# ==========================================
# 2. 配置跨域资源共享 (CORS) - 绝对不能漏！
# ==========================================
# 前端 Vue 运行在 5173 端口，后端运行在 8000 端口。
# 浏览器默认会拦截不同端口之间的请求（跨域限制）。这几行代码是放行通行证。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源，上线后可改为前端的真实域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. 数据模型定义 (Pydantic)
# ==========================================
# 用于限制和校验前端传过来的数据格式，写错了直接报错，免去写 if-else
class SubmitCodeRequest(BaseModel):
    problem_id: int
    language: str  # 例如: "cpp", "python", "java"
    code: str  # 具体的代码字符串


class ProblemResponse(BaseModel):
    id: int
    title: str
    difficulty: str


# 模拟数据库（假数据，后期这里会换成读取 SQLite）
MOCK_PROBLEMS = [
    {"id": 1000, "title": "A+B Problem", "difficulty": "入门"},
    {"id": 1001, "title": "两数之和", "difficulty": "普及-"},
    {"id": 1002, "title": "动态规划基础", "difficulty": "提高+/省选-"}
]


# ==========================================
# 4. 后台核心逻辑 (评测沙箱占位)
# ==========================================
async def run_judger_worker(submission_id: int, code: str, lang: str):
    """
    这是一个异步后台任务。未来这里会通过 subprocess 去调用你的 C++ 评测机。
    """
    print(f"[评测机] 正在编译运行提交 #{submission_id}, 语言: {lang}...")
    await asyncio.sleep(2)  # 模拟沙箱评测花费了 2 秒钟
    print(f"[评测机] 提交 #{submission_id} 评测完成！结果: AC (Accepted)")
    # 真实场景下，跑出结果后，这里会用 SQL 把数据库里的状态更新为 AC


# ==========================================
# 5. API 路由设计 (Endpoints)
# ==========================================

# --- 系统探针接口 ---
@app.get("/")
async def root():
    return {"message": "Hello, 洛谷青年！OJ Backend 正常运行中！"}


# --- 题目相关接口 ---
@app.get("/api/problems", response_model=list[ProblemResponse])
async def get_problem_list():
    """获取全站题目列表"""
    return MOCK_PROBLEMS


@app.get("/api/problems/{problem_id}")
async def get_problem_detail(problem_id: int):
    """获取单道题目的详情"""
    for p in MOCK_PROBLEMS:
        if p["id"] == problem_id:
            return p
    # 如果没找到这道题，直接返回 404
    raise HTTPException(status_code=404, detail="题目不存在或已被隐藏")


# --- 核心业务：提交代码 ---
@app.post("/api/submit")
async def submit_code(req: SubmitCodeRequest, background_tasks: BackgroundTasks):
    """用户在前端点击'提交代码'时触发的接口"""

    # 1. (未来) 将用户的提交信息存入 SQLite，生成一个自增的提交 ID，状态为 Pending
    mock_submission_id = 9527

    # 2. 将代码丢给后台去慢慢评测 (不阻塞主线程，网页可以瞬间拿到响应)
    background_tasks.add_task(run_judger_worker, mock_submission_id, req.code, req.language)

    # 3. 立即回复前端
    return {
        "message": "代码已提交，评测排队中...",
        "submission_id": mock_submission_id,
        "status": "Pending"
    }