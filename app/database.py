import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Load the ENV Variables
load_dotenv()


DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASS = 1102
DB_NAME = 'urls_short'

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get the database session
def get_db():
    """
    Returns a database session. 
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()