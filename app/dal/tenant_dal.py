# tenant_dal.py

from sqlalchemy.orm import Session
from app.models.tenant import TenantPersonalDetails, TenantPreferenceDetails
from dataclasses import asdict
from sqlalchemy import text
from app.db_queries import *

# CRUD for tenant_personal_details
def get_tenant(db: Session, user_id: int):
    return db.query(TenantPersonalDetails).filter(TenantPersonalDetails.user_id == user_id).first()

def create_tenant(db: Session, tenant: TenantPersonalDetails):
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

def update_tenant(db: Session, user_id: int, tenant_update_data: dict):
    tenant = db.query(TenantPersonalDetails).filter(TenantPersonalDetails.user_id == user_id).first()
    if tenant:
        for key, value in tenant_update_data.items():
            setattr(tenant, key, value)
        db.commit()
    return tenant

def delete_tenant(db: Session, user_id: int):
    tenant = db.query(TenantPersonalDetails).filter(TenantPersonalDetails.user_id == user_id).first()
    if tenant:
        db.delete(tenant)
        db.commit()
    return tenant

def get_all_tenants(db: Session):
    """Retrieve all tenants."""
    return db.query(TenantPersonalDetails).all()

def get_tenant_by_email(db: Session, email: str):
    """Retrieve a tenant by email."""
    return db.query(TenantPersonalDetails).filter(TenantPersonalDetails.email == email).first()

def get_tenants_by_province(db: Session, province: str):
    """Retrieve tenants by province."""
    return db.query(TenantPersonalDetails).filter(TenantPersonalDetails.province == province).all()

# CRUD for tenant_property_preferences
def create_property_preference(db: Session, preference: TenantPreferenceDetails):
    db.add(preference)
    db.commit()
    db.refresh(preference)
    return preference

def get_property_preference(db: Session, preference_id: int):
    """Retrieve property preference by ID."""
    return db.query(TenantPreferenceDetails).filter(TenantPreferenceDetails.id == preference_id).first()

def get_preferences_by_user(db: Session, user_id: int):
    """Retrieve all property preferences for a specific user."""
    return db.query(TenantPreferenceDetails).filter(TenantPreferenceDetails.user_id == user_id).all()

def get_preferences_by_session(db: Session, session_id: str):
    """Retrieve all property preferences for a specific session."""
    return db.query(TenantPreferenceDetails).filter(TenantPreferenceDetails.session_id == session_id).all()

# app/data_access_objects/daos.py
import json
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

# UPSERT query for tenant preferences (wrapped with `text()`)
#-- Insert a new record or update the existing record based on is_logged_in status
UPSERT_TENANT_PREFERENCES = text("""
INSERT INTO tenant_preference_details (
    user_id, session_id, tenant_category_id, location_category_id, budget_category_id,
    school_proximity, hospital_proximity, transit_proximity, in_house_laundry,
    gym, pet_friendly, pool, is_logged_in
)
VALUES (
    COALESCE(:user_id, NULL), :session_id, :tenant_category_id, :location_category_id, :budget_category_id,
    :school_proximity, :hospital_proximity, :transit_proximity, :in_house_laundry,
    :gym, :pet_friendly, :pool, :is_logged_in
)
ON DUPLICATE KEY UPDATE
    -- If is_logged_in is false, update session_id only
    session_id = IF(VALUES(is_logged_in) = FALSE, VALUES(session_id), session_id),
    -- If is_logged_in is true, update user_id only
    user_id = IF(VALUES(is_logged_in) = TRUE, VALUES(user_id), user_id),
    -- Always update these fields regardless of is_logged_in status
    tenant_category_id = VALUES(tenant_category_id),
    location_category_id = VALUES(location_category_id),
    budget_category_id = VALUES(budget_category_id),
    school_proximity = VALUES(school_proximity),
    hospital_proximity = VALUES(hospital_proximity),
    transit_proximity = VALUES(transit_proximity),
    in_house_laundry = VALUES(in_house_laundry),
    gym = VALUES(gym),
    pet_friendly = VALUES(pet_friendly),
    pool = VALUES(pool),
    is_logged_in = VALUES(is_logged_in);
""")

def upsert_preferences_to_db(db: Session, json_data: str):
    """
    Data Access Layer function to save or update tenant preferences to the database.
    It performs an UPSERT query to insert or update the preferences.
    """
    
    # Convert the JSON string to a Python dictionary
    #preferences = json.loads(json_data)
    
    # Convert JSON string to a dictionary
    data_dict = json.loads(json_data)

    # Extract the relevant keys and values dynamically
    params = {key: value for key, value in data_dict.items() if key in [
        "user_id", "session_id", "tenant_category_id", "location_category_id", 
        "budget_category_id", "school_proximity", "hospital_proximity", 
        "transit_proximity", "in_house_laundry", "gym", "pet_friendly", 
        "pool", "is_logged_in"
    ]}
    
    # Execute the UPSERT query using SQLAlchemy raw connection
    
    db.execute(UPSERT_TENANT_PREFERENCES, params)
    
    db.commit()  # Commit the transaction to the database
   
    return True