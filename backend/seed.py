# import os
from pathlib import Path
# from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Problem, TestCase

# Create tables just in case
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create user
user = db.query(User).filter(User.id == 1).first()
if not user:
    user = User(id=1, username="test_user", hashed_password="fake")
    db.add(user)

# Create problem
problem = db.query(Problem).filter(Problem.id == 1001).first()
if not problem:
    problem = Problem(id=1001, title="A+B Problem", difficulty="入门", description="输入两个整数 a 和 b，输出它们的和。")
    db.add(problem)

# Create test case files
data_dir = Path("data/problems/1001")
data_dir.mkdir(parents=True, exist_ok=True)
in_file = data_dir / "1.in"
out_file = data_dir / "1.out"
in_file.write_text("1 2\n", encoding="utf-8")
out_file.write_text("3\n", encoding="utf-8")

# Create TestCase
tc = db.query(TestCase).filter(TestCase.problem_id == 1001, TestCase.sort_order == 1).first()
if not tc:
    tc = TestCase(problem_id=1001, input_path="data/problems/1001/1.in", output_path="data/problems/1001/1.out", sort_order=1)
    db.add(tc)

db.commit()
print("Database seeded with mock User (id=1) and Problem (id=1001).")
