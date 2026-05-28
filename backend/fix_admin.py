from database import SessionLocal
from models import User
from auth import get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.username == "test_user").first()
if not admin:
    admin = User(username="test_user", role="admin")
    db.add(admin)

admin.hashed_password = get_password_hash("123456")
admin.role = "admin"
db.commit()
print(f"Admin {admin.username} password reset to 123456")
