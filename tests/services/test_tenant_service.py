import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database_connect import Base
from app.services.tenant_service import save_preferences_service
from app.models.tenant import *

# Configure a connection to the test database
DATABASE_URL = "mysql+pymysql://root:root123@localhost/trace_rent_ai"  # Adjust credentials as needed

# Create an engine and session for the test database
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database schema for tests
Base.metadata.create_all(bind=engine)

def test_save_preferences_to_db_integration():
    # Set up a new database session
    db = TestingSessionLocal()

    try:
        # Sample JSON data for the test
        json_data = json.dumps({
            "in_house_laundry": False,
            "gym": False,
            "pet_friendly": False,
            "pool": False,
            "is_logged_in": False,
            "user_id": 1,
            "tenant_category_id": 1,
            "location_category_id": 1,
            "budget_category_id": 1,
            "school_proximity": 1,
            "hospital_proximity": 2,
            "transit_proximity": 5,
            "session_id": "1"
        })
        
        # Call the function to save preferences to the database
        save_preferences_service(db, json_data)

        # Commit the session (to ensure that changes are saved in the database)
        db.commit()

        # Retrieve the saved preferences from the database
        saved_preferences = db.query(TenantPreferenceDetails).filter_by(user_id=1).first()

        # Assertions
        assert saved_preferences is not None
        assert saved_preferences.in_house_laundry == False
        assert saved_preferences.gym == False
        assert saved_preferences.pet_friendly == False
        assert saved_preferences.pool == False
        assert saved_preferences.user_id == 1

    except Exception as e:
        print(f"Test failed due to: {e}")
        raise
    finally:
        # Optionally, you can clean up after the test if necessary
        db.close()