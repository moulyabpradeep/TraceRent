from sqlalchemy import Column, Integer, String
from app.database_connect import Base
from app.data_access_objects.daos import UserData
from app.global_constants import (  # Importing from constants
    USER_TABLE
)

class User(Base):
    __tablename__ = USER_TABLE  # Use constant for table name

    user_id = Column(Integer, primary_key=True, index=True)  # Primary key
    username = Column(String(255), unique=True, index=True)  # Unique username
    password = Column(String(255))  # User password
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(15))  # +1(226)999-9999
    
    @staticmethod
    def from_user_data(user_data: 'UserData') -> 'User':
        """
        Convert a UserData instance to a User instance by mapping the fields.
        """
        return User(
            user_id=user_data.user_id,
            name=user_data.name_of_user,
            password=user_data.user_password,
            email=user_data.user_email,
            username=user_data.user_email,
            phone=user_data.user_phone
        )

    @staticmethod
    def from_json(json_data: dict) -> 'User':
        # Unpack the dictionary directly into the model fields
        return User(**json_data)

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
