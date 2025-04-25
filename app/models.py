import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, DateTime, func

Base = declarative_base()

class URL(Base):
    """
    Represents the 'urls' table in the database.
    """
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    long_url = Column(Text, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<URL(long_url='{self.long_url}', short_code='{self.short_code}')>"