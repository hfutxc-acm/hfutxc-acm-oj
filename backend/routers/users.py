from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import uuid
import shutil
from pathlib import Path

from database import get_db, PROJECT_ROOT
from models import User
from dependencies import get_current_user

router = APIRouter(tags=["users"])

AVATAR_DIR = PROJECT_ROOT / "data" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/api/users/{user_id}")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "groups": [{"id": g.id, "name": g.name} for g in user.groups],
        "submissions_count": len(user.submissions),
        "ac_count": len([s for s in user.submissions if s.status == "OK"])
    }

@router.post("/api/users/{user_id}/avatar")
async def upload_avatar(user_id: int, file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权修改他人头像")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传有效的图片文件")
    
    ext = file.filename.split(".")[-1] if "." in file.filename else "png"
    filename = f"avatar_{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = AVATAR_DIR / filename
    
    with filepath.open("wb") as out:
        shutil.copyfileobj(file.file, out)
        
    user.avatar_url = f"/api/uploads/avatars/{filename}"
    db.commit()
    return {"message": "头像上传成功", "avatar_url": user.avatar_url}
