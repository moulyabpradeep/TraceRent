# user_service.py

from sqlalchemy.orm import Session
from app.dal.user_dal import (
    save_user_to_db, 
    get_user_from_db
)
from models import UserData

# Save a user to the database
def user_sign_up(db: Session, user_data: UserData) -> int:
    # Directly pass UserData object to dal method
    return save_user_to_db(db, user_data)

# Get a user from the database by email
def user_login(db: Session, user_email: str) -> UserData:
    user_record = get_user_from_db(db, user_email)
    # Return UserData object directly if record found
    return UserData.from_json(user_record.to_json()) if user_record else None