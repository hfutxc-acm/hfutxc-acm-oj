from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from pydantic import BaseModel

from database import get_db
from models import Group, User
from dependencies import get_current_user

router = APIRouter(tags=["groups"])

class GroupCreate(BaseModel):
    name: str
    description: str = ""

@router.get("/api/groups")
async def get_groups(db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(Group))
    groups = result.all()
    return [{"id": g.id, "name": g.name, "description": g.description} for g in groups]

@router.post("/api/groups")
async def create_group(group: GroupCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(Group).where(Group.name == group.name))
    if result.first():
        raise HTTPException(status_code=400, detail="组织名已存在")
    new_group = Group(name=group.name, description=group.description, owner_id=current_user.id)
    db.add(new_group)
    current_user.groups.append(new_group)
    await db.commit()
    await db.refresh(new_group)
    return {"message": "创建成功", "group": {"id": new_group.id, "name": new_group.name}}

@router.post("/api/groups/{group_id}/join")
async def join_group(group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(Group).where(Group.id == group_id))
    group = result.first()
    if not group:
        raise HTTPException(status_code=404, detail="组织不存在")
    if group not in current_user.groups:
        current_user.groups.append(group)
        await db.commit()
    return {"message": "成功加入组织"}

@router.post("/api/groups/{group_id}/leave")
async def leave_group(group_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(Group).where(Group.id == group_id))
    group = result.first()
    if not group:
        raise HTTPException(status_code=404, detail="组织不存在")
    if group in current_user.groups:
        current_user.groups.remove(group)
        await db.commit()
    return {"message": "成功退出组织"}
