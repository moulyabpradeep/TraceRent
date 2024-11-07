from sqlalchemy.orm import Session
from models import User
from dataobjects.data_objects import UserData
# Save a user to the database and return the user ID
def save_user_to_db(db: Session, user_data: UserData) -> int:
    new_user = User(**user_data.__dict__)  # Directly unpack UserData into User
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.user_id


# Retrieve a user from the database by email
def get_user_from_db(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()