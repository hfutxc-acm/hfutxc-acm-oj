from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from database import get_db
from models import User
from dependencies import check_admin_role, check_super_admin_role

router = APIRouter(tags=["admin"])

@router.get("/api/admin/users")
async def get_all_users(current_user: User = Depends(check_admin_role), db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(User))
    users = result.all()
    return [{
        "id": u.id,
        "username": u.username,
        "role": u.role,
        "avatar_url": u.avatar_url,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "groups": [{"id": g.id, "name": g.name} for g in u.groups]
    } for u in users]

@router.put("/api/admin/users/{user_id}/role")
async def update_user_role(user_id: int, role: str = Body(embed=True), current_user: User = Depends(check_super_admin_role), db: AsyncSession = Depends(get_db)):
    if role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="无效的角色")
    result = await db.exec(select(User).where(User.id == user_id))
    user = result.first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能直接修改自己的角色，如果是交接超管请使用专属接口")
    if user.role == "super_admin":
        raise HTTPException(status_code=400, detail="不能修改超级管理员的角色")
    
    user.role = role
    await db.commit()
    return {"message": "角色更新成功", "role": user.role}

@router.post("/api/admin/transfer_super_admin/{user_id}")
async def transfer_super_admin(user_id: int, current_user: User = Depends(check_super_admin_role), db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(User).where(User.id == user_id))
    user = result.first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="不能将超级管理员移交给本人")
    
    # 权力交接
    user.role = "super_admin"
    current_user.role = "admin"
    
    await db.commit()
    return {"message": "交接成功", "new_super_admin_id": user.id}
