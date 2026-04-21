from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# engine handles the actual connection to Railway
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True
)

# SessionLocal is what we use in our routes to talk to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)