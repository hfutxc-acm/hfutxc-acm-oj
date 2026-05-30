from database import SessionLocal
from models import User
from auth import get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.username == "admin").first()
if not admin:
    admin = User(username="admin", role="super_admin")
    db.add(admin)

admin.hashed_password = get_password_hash("admin")
admin.role = "super_admin"
db.commit()
print(f"Super admin {admin.username} created/updated with password 'admin'")
