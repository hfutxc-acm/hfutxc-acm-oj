import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy import text
from pathlib import Path

# 1. 定义数据库文件的存储路径
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
DATABASE_PATH = DATA_DIR / "oj.db"
# 使用 aiosqlite 作为异步驱动
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH.as_posix()}"

# 2. 创建异步数据库引擎
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)

from sqlalchemy import event
from sqlalchemy.engine import Engine

# SQLite 专属：开启 WAL 模式提高并发性能
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

# 3. 创建异步会话工厂
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 4. 初始化数据库表的函数
async def init_db():
    async with engine.begin() as conn:
        # SQLModel.metadata.create_all 需要同步环境，因此用 run_sync
        await conn.run_sync(SQLModel.metadata.create_all)
        # 自动迁移：给已有表添加新字段（SQLite 的 ALTER TABLE 幂等处理）
        for col, default in [("time_ms", "0"), ("memory_kb", "0")]:
            try:
                await conn.execute(text(f"ALTER TABLE submissions ADD COLUMN {col} INTEGER DEFAULT {default}"))
            except Exception:
                pass  # 列已存在，忽略

# 5. FastAPI 依赖项：每个请求独立的异步会话
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
