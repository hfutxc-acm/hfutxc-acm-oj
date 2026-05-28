from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

try:
    from .database import Base
except ImportError:
    from database import Base

user_groups_table = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("joined_at", DateTime, default=datetime.utcnow)
)

class Group(Base):
    """用户组/战队/班级"""
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, default="")
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True) # 谁创建的这个组
    created_at = Column(DateTime, default=datetime.utcnow)
    
    users = relationship("User", secondary=user_groups_table, back_populates="groups")

class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # 角色: 'admin' (系统管理员/教师), 'user' (普通学生)
    role = Column(String, default="user")
    
    # 头像
    avatar_url = Column(String, default="")
    
    # 所加入的所有组
    groups = relationship("Group", secondary=user_groups_table, back_populates="users")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    submissions = relationship("Submission", back_populates="user")


class Problem(Base):
    """题目表"""
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    description = Column(Text, nullable=True)  # 改用 Text 支撑长篇大论的题面描述
    input_description = Column(Text, nullable=True)
    output_description = Column(Text, nullable=True)
    time_limit_ms = Column(Integer, default=1000, nullable=False)
    memory_limit_mb = Column(Integer, default=256, nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 建立关联：一道题目可以被多次提交
    submissions = relationship("Submission", back_populates="problem")
    testcases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")


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
    results = relationship("SubmissionResult", back_populates="submission", cascade="all, delete-orphan")


class TestCase(Base):
    """题目测试点表"""
    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    input_path = Column(String, nullable=False)
    output_path = Column(String, nullable=False)
    score = Column(Integer, default=10, nullable=False)
    sort_order = Column(Integer, nullable=False)
    is_sample = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    problem = relationship("Problem", back_populates="testcases")
    results = relationship("SubmissionResult", back_populates="testcase")


class SubmissionResult(Base):
    """单个提交在每个测试点上的结果"""
    __tablename__ = "submission_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    testcase_id = Column(Integer, ForeignKey("testcases.id"), nullable=False)
    status = Column(String, nullable=False)
    time_ms = Column(Integer, default=0, nullable=False)
    memory_kb = Column(Integer, default=0, nullable=False)
    message = Column(Text, nullable=True)

    submission = relationship("Submission", back_populates="results")
    testcase = relationship("TestCase", back_populates="results")
