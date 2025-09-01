from app.db import Base, engine
from app import models

print("📦 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
