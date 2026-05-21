from sqlalchemy import Column, Integer, String
from .database import Base

class Problem(Base):
    """题目数据库模型"""
    __tablename__ = "problems"  # 在数据库里的真实表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    description = Column(String, nullable=True)  # 题目描述字段，先预留