from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from models import User, Problem, Submission, SubmissionResult, TestCase, Group
from auth import verify_password, create_access_token, decode_access_token
from database import async_session_maker

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        
        async with async_session_maker() as db:
            result = await db.exec(select(User).where(User.username == username))
            user = result.first()
            if not user or not verify_password(password, user.password_hash):
                return False
            
            # 仅允许 super_admin 访问 sqladmin 后台
            if user.role != "super_admin":
                return False
            
            # 使用现有逻辑生成 token，存入 session 方便 sqladmin 验证
            token = create_access_token(data={"sub": user.username, "role": user.role, "id": user.id})
            request.session.update({"token": token})
        
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        
        payload = decode_access_token(token)
        if not payload or payload.get("role") != "super_admin":
            return False
            
        return True

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role, User.created_at]
    column_searchable_list = [User.username]
    column_sortable_list = [User.id, User.created_at]
    icon = "fa-solid fa-user"

class ProblemAdmin(ModelView, model=Problem):
    column_list = [Problem.id, Problem.title, Problem.difficulty, Problem.is_public, Problem.created_at]
    column_searchable_list = [Problem.title]
    column_sortable_list = [Problem.id, Problem.difficulty, Problem.created_at]
    icon = "fa-solid fa-book"

class SubmissionAdmin(ModelView, model=Submission):
    column_list = [Submission.id, Submission.user_id, Submission.problem_id, Submission.language, Submission.status, Submission.created_at]
    column_searchable_list = [Submission.language, Submission.status]
    column_sortable_list = [Submission.id, Submission.created_at]
    icon = "fa-solid fa-code"
    
class TestCaseAdmin(ModelView, model=TestCase):
    column_list = [TestCase.id, TestCase.problem_id, TestCase.sort_order, TestCase.is_sample, TestCase.score]
    icon = "fa-solid fa-vial"

class GroupAdmin(ModelView, model=Group):
    column_list = [Group.id, Group.name, Group.owner_id, Group.created_at]
    column_searchable_list = [Group.name]
    icon = "fa-solid fa-users"

def init_admin(app, engine):
    authentication_backend = AdminAuth(secret_key="oj-super-secret-key-for-admin")
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend, title="OJ Admin Panel")
    
    admin.add_view(UserAdmin)
    admin.add_view(ProblemAdmin)
    admin.add_view(SubmissionAdmin)
    admin.add_view(TestCaseAdmin)
    admin.add_view(GroupAdmin)
