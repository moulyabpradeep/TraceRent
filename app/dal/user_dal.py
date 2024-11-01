from sqlalchemy.orm import Session
from app.models import User  # Assuming you have a User model defined in app.models.user

# CRUD for users

def get_user(db: Session, user_id: int):
    """Retrieve a user by user ID."""
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, user: User):
    """Create a new user record."""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user_id: int, user_update_data: dict):
    """Update user details based on user ID."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        for key, value in user_update_data.items():
            setattr(user, key, value)
        db.commit()
    return user

def delete_user(db: Session, user_id: int):
    """Delete a user by user ID."""
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def get_all_users(db: Session):
    """Retrieve all users."""
    return db.query(User).all()

def get_user_by_username(db: Session, username: str):
    """Retrieve a user by username."""
    return db.query(User).filter(User.username == username).first()