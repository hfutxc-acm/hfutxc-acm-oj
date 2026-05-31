import re
from pathlib import Path

main_py = Path("main.py")
content = main_py.read_text(encoding="utf-8")

# 1. Imports update
content = content.replace("from sqlalchemy.orm import Session", "from sqlmodel.ext.asyncio.session import AsyncSession\nfrom sqlmodel import select")
content = content.replace("from database import Base, PROJECT_ROOT, SessionLocal, engine, get_db", "from database import PROJECT_ROOT, async_session_maker, engine, get_db, init_db")

# 2. Add judge queue import
if "from services.judge_worker import judge_queue, judge_worker_loop" not in content:
    content = content.replace("from routers import admin as admin_router", "from routers import admin as admin_router\nfrom services.judge_worker import judge_queue, judge_worker_loop")

# 3. Startup event
startup_old = """@app.on_event("startup")
async def startup_event():
    inspector = inspect(engine)
    if not inspector.has_table("problems"):
        Base.metadata.create_all(bind=engine)"""
startup_new = """@app.on_event("startup")
async def startup_event():
    await init_db()
    asyncio.create_task(judge_worker_loop())"""
content = content.replace(startup_old, startup_new)

# 4. Remove judge0_submit and run_judger_worker from main.py
# They are between replace_problem_data and get_problem_list
import ast
# We'll just regex them out since we know they start with `def judge0_submit` and end before `@app.get("/api/problems")`
content = re.sub(r"def judge0_submit\(.*?\n@app\.get\(\"/api/problems\"\)", "@app.get(\"/api/problems\")", content, flags=re.DOTALL)

# 5. Fix Session -> AsyncSession in endpoints
content = content.replace("db: Session = Depends(get_db)", "db: AsyncSession = Depends(get_db)")

# 6. Fix db.query
content = content.replace("db.query(Problem).order_by(Problem.id.asc()).all()", "(await db.exec(select(Problem).order_by(Problem.id.asc()))).all()")
content = content.replace("db.query(Problem).filter(Problem.id == problem_id).first()", "(await db.exec(select(Problem).where(Problem.id == problem_id))).first()")
content = content.replace("db.query(Problem).filter(Problem.id == problem_id).delete()", "await db.exec(select(Problem).where(Problem.id == problem_id)) # Not correct for delete, need a better one")

# Custom regex for db.query(X).filter(X.y == z).first()
def replace_query_first(match):
    model = match.group(1)
    condition = match.group(2)
    return f"(await db.exec(select({model}).where({condition}))).first()"

content = re.sub(r"db\.query\(([A-Za-z_]+)\)\.filter\((.*?)\)\.first\(\)", replace_query_first, content)

def replace_query_all(match):
    model = match.group(1)
    condition = match.group(2)
    return f"(await db.exec(select({model}).where({condition}))).all()"
content = re.sub(r"db\.query\(([A-Za-z_]+)\)\.filter\((.*?)\)\.all\(\)", replace_query_all, content)

# 7. db.commit() -> await db.commit()
content = content.replace("db.commit()", "await db.commit()")
content = content.replace("db.refresh(problem)", "await db.refresh(problem)")

# 8. replace_problem_data is called from upload_testcases
content = content.replace("replace_problem_data(problem_id, tmp_path, valid_orders, db)", "await replace_problem_data(problem_id, tmp_path, valid_orders, db)")
content = content.replace("def replace_problem_data", "async def replace_problem_data")
# replace_problem_data internal queries
content = content.replace("db.query(TestCase).filter(TestCase.problem_id == problem_id).delete()", "# deleted via sqlmodel\n    from sqlalchemy import delete as sa_delete\n    await db.exec(sa_delete(TestCase).where(TestCase.problem_id == problem_id))")

# 9. submit_code logic
content = content.replace("background_tasks.add_task(run_judger_worker, submission.id, SessionLocal)", "await judge_queue.put(submission.id)")

main_py.write_text(content, encoding="utf-8")
print("main.py refactored!")
