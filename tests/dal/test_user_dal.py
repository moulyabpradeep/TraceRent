from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import *  # Ensure your User model is correctly defined
from app.dal.user_dal import (
    create_user,
    get_user,
    update_user,
    delete_user,
    get_all_users,
)
import configparser

import pytest
# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get database connection URL
db_config = {
    'host': config['database']['host'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'database': config['database']['database']
}
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Database setup for testing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture for database session
@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

# Test cases
# Testing CRUD operations
def test_user_operations():

    # Create a user
    new_user = User(user_id=1, username='test_user', password='test_password')
    created_user = create_user(db_session, new_user)
    print(f"Created User: {created_user}")

    # Get user
    user = get_user(db_session, 1)
    print(f"Retrieved User: {user}")

    # Update user
    updated_user = update_user(db_session, 1, {'username': 'updated_user', 'password': 'updated_password'})
    print(f"Updated User: {updated_user}")

    # Get all users
    all_users = get_all_users(db_session)
    print(f"All Users: {all_users}")

    # Delete user
    deleted_user = delete_user(db_session, 1)
    print(f"Deleted User: {deleted_user}")

    db_session.close()

if __name__ == "__main__":
    test_user_operations()
