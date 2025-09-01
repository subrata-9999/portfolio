from app.db import SessionLocal
from app.models import Admin
from app.auth import hash_password  # your hash function

db = SessionLocal()

# Create admin with hashed password automatically
new_admin = Admin(username="", password=hash_password(""))
db.add(new_admin)
db.commit()
db.close()

print("✅ Admin inserted successfully!")
