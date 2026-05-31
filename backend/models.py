from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, Text

class UserGroupLink(SQLModel, table=True):
    __tablename__ = "user_groups"
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    group_id: Optional[int] = Field(default=None, foreign_key="groups.id", primary_key=True)
    joined_at: datetime = Field(default_factory=datetime.utcnow)

class Group(SQLModel, table=True):
    __tablename__ = "groups"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str = Field(default="")
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    users: List["User"] = Relationship(back_populates="groups", link_model=UserGroupLink)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    
    role: str = Field(default="user")
    avatar_url: str = Field(default="")
    
    groups: List[Group] = Relationship(back_populates="users", link_model=UserGroupLink)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    submissions: List["Submission"] = Relationship(back_populates="user")


class Problem(SQLModel, table=True):
    __tablename__ = "problems"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    difficulty: str
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    input_description: Optional[str] = Field(default=None, sa_column=Column(Text))
    output_description: Optional[str] = Field(default=None, sa_column=Column(Text))
    time_limit_ms: int = Field(default=1000)
    memory_limit_mb: int = Field(default=256)
    is_public: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    submissions: List["Submission"] = Relationship(back_populates="problem")
    testcases: List["TestCase"] = Relationship(back_populates="problem")


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    problem_id: int = Field(foreign_key="problems.id")

    language: str
    code: str = Field(sa_column=Column(Text))
    status: str = Field(default="Pending")
    time_ms: int = Field(default=0)
    memory_kb: int = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="submissions")
    problem: Optional[Problem] = Relationship(back_populates="submissions")
    results: List["SubmissionResult"] = Relationship(back_populates="submission")


class TestCase(SQLModel, table=True):
    __tablename__ = "testcases"

    id: Optional[int] = Field(default=None, primary_key=True)
    problem_id: int = Field(foreign_key="problems.id")
    input_path: str
    output_path: str
    score: int = Field(default=10)
    sort_order: int
    is_sample: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    problem: Optional[Problem] = Relationship(back_populates="testcases")
    results: List["SubmissionResult"] = Relationship(back_populates="testcase")


class SubmissionResult(SQLModel, table=True):
    __tablename__ = "submission_results"

    id: Optional[int] = Field(default=None, primary_key=True)
    submission_id: int = Field(foreign_key="submissions.id")
    testcase_id: int = Field(foreign_key="testcases.id")
    status: str
    time_ms: int = Field(default=0)
    memory_kb: int = Field(default=0)
    message: Optional[str] = Field(default=None, sa_column=Column(Text))

    submission: Optional[Submission] = Relationship(back_populates="results")
    testcase: Optional[TestCase] = Relationship(back_populates="results")
