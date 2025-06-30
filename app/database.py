from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://iot_user:iot_password@localhost:5432/iot_heartbeat"
)

def create_db_engine():
    """Create database engine with retry logic"""
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Enable connection health checks
        pool_recycle=300,    # Recycle connections every 5 minutes
        echo=False           # Set to True for SQL debugging
    )

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def wait_for_db(max_retries=30, retry_interval=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            # Try to connect to the database using proper SQLAlchemy syntax
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            print(f"✅ Database connection established on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"⏳ Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_interval)
            else:
                print("❌ Failed to connect to database after all retries")
                return False

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 