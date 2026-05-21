from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 定义数据库文件的存储路径（在当前目录下生成一个 oj.db 文件）
SQLALCHEMY_DATABASE_URL = "sqlite:///./oj.db"

# 2. 创建数据库引擎
# connect_args={"check_same_thread": False} 是 SQLite 专属配置
# 允许 FastAPI 的多个异步线程同时访问同一个 SQLite 数据库文件
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. 创建会话工厂，未来每次增删改查都会用到一个 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建基类，未来所有的数据库模型（表）都要继承它
Base = declarative_base()

# 5. 依赖项：每个请求独立的数据库会话，用完自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()