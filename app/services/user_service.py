# user_service.py
from app.services.tenant_service import update_user_id_in_preferences
from app.dal.user_dal import (
    save_user_to_db, 
    get_user_from_db
)
from app.models.user import Users

from app.database_connect import SessionLocal

# Save a user to the database
def user_sign_up(user_data: Users) -> int:
    # Directly pass UserData object to dal method
    db = SessionLocal()
    try:
        #save_user_to_db(db, user_data)
        user_id=save_user_to_db(db, user_data)
        if(user_id):
            if(update_user_id_in_preferences(user_id, user_data['session_id'], True)):
                return user_id
            else:
                0
            
    finally:
        db.close()

# Get a user from the database by email        
def get_user_by_username(user_email: str) -> dict:
    db = SessionLocal()
    try:
        user_record = get_user_from_db(db, user_email)
        # Use to_dict if user_record is found
        return user_record.to_dict() if user_record else None
    finally:
        db.close()
