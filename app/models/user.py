from sqlalchemy import Column, Integer, String
from app.database_connect import Base
from app.global_constants import (  # Importing from constants
    USER_TABLE
)

class Users(Base):
    __tablename__ = USER_TABLE  # Use constant for table name

    user_id = Column(Integer, primary_key=True, index=True)  # Primary key
    username = Column(String(255), unique=True, index=True)  # Unique username
    password = Column(String(255))  # User password
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(15)) # +1(226)999-9999
    
    @staticmethod
    def from_json(json_data: dict) -> 'Users':
        # Unpack the dictionary directly into the model fields
        return Users(**json_data)

    def to_dict(self) -> dict:
        # Convert the User object to a dictionary
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }