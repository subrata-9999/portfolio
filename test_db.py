from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection failed!")
    print(e)
