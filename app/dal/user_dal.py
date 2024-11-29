from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy import update

# Save a user to the database and return the user ID
def save_user_to_db(db: Session, user_data: User) -> int:
    
    new_user = User(
        username=user_data['user_email'],
        password=user_data['user_password'],
        name=user_data['name_of_user'],
        email=user_data['user_email'],
        phone=user_data['user_phone']
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.user_id


# Retrieve a user from the database by email
def get_user_from_db(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def update_user_info(db: Session, user_data: User)-> bool:
    # Prepare fields to update only if they are not None
    fields_to_update = {}
    
    if user_data.name is not None:
        fields_to_update['name'] = user_data.name
    if user_data.email is not None:
        fields_to_update['email'] = user_data.email
        fields_to_update['username'] = user_data.email
    if user_data.password is not None:
        fields_to_update['password'] = user_data.password
    if user_data.phone is not None:
        fields_to_update['phone'] = user_data.phone
    if user_data.user_id is not None:
        user_id = user_data.user_id
    

    # Only perform the update if there are fields to update
    if fields_to_update:
        result = db.execute(
            update(User).
            where(User.user_id == user_id).
            values(**fields_to_update)
        )
        db.commit()
        
        # Check if any rows were updated
        return result.rowcount > 0

    return False  # Return False if no fields were provided for update



def update_user_password(db: Session, user_data: User)-> bool:
    # Prepare fields to update only if they are not None
    fields_to_update = {}
   
    if user_data.password is not None:
        fields_to_update['password'] = user_data.password
    if user_data.user_id is not None:
        user_id = user_data.user_id
    
    # Only perform the update if there are fields to update
    if fields_to_update:
        result = db.execute(
            update(User).
            where(User.user_id == user_id).
            values(**fields_to_update)
        )
        db.commit()
        
        # Check if any rows were updated
        return result.rowcount > 0

    return False  # Return False if no fields were provided for update
