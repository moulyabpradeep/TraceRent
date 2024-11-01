from sqlalchemy import Column, Integer, String
from app.database import Base
from app.global_constants import (  # Importing from constants
    USER_TABLE
)

class User(Base):
    __tablename__ = USER_TABLE  # Use constant for table name

    user_id = Column(Integer, primary_key=True, index=True)  # Primary key
    username = Column(String(255), unique=True, index=True)  # Unique username
    password = Column(String(255))  # User password