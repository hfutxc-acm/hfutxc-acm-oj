from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    # 注意：实际工程中绝不能存明文密码，这里先留出 hashed 密码字段，后续引入加密
    hashed_password = Column(String, nullable=False)

    # 建立关联：一个用户可以有多次代码提交
    submissions = relationship("Submission", back_populates="user")


class Problem(Base):
    """题目表"""
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # 改用 Text 支撑长篇大论的题面描述

    # 建立关联：一道题目可以被多次提交
    submissions = relationship("Submission", back_populates="problem")


class Submission(Base):
    """提交记录表（核心纽带）"""
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # 外键关联：关联到用户表的 id 和题目表的 id
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)

    language = Column(String, nullable=False)  # cpp, python, java 等
    code = Column(Text, nullable=False)  # 用户提交的源代码
    status = Column(String, default="Pending")  # Pending, AC, WA, TLE, RE 等

    # 记录提交时间，全自动记录
    created_at = Column(DateTime, default=datetime.utcnow)

    # 反向引用：通过 submission.user 就能直接拿到该用户的对象，极其方便
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")