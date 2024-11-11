# tenant_dal.py

from sqlalchemy.orm import Session
from app.models.tenant import TenantPersonalDetails, TenantPreferenceDetails
from sqlalchemy import text
from app.db_queries import *
import json

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

# First, attempt the insert or update based on the unique key constraint (user_id, session_id)
upsert_preferences_session_id_query = text("""
INSERT INTO `tenant_preference_details` (
    `user_id`,
    `session_id`,
    `tenant_category_id`,
    `location_category_id`,
    `budget_category_id`,
    `school_proximity`,
    `hospital_proximity`,
    `transit_proximity`,
    `in_house_laundry`,
    `gym`,
    `pet_friendly`,
    `pool`,
    `is_logged_in`
)
VALUES (
    COALESCE(:user_id, NULL), :session_id, :tenant_category_id, :location_category_id, :budget_category_id,
    :school_proximity, :hospital_proximity, :transit_proximity, :in_house_laundry,
    :gym, :pet_friendly, :pool, :is_logged_in
)
ON DUPLICATE KEY UPDATE
    `user_id` = VALUES(`user_id`),
    `tenant_category_id` = VALUES(`tenant_category_id`),
    `location_category_id` = VALUES(`location_category_id`),
    `budget_category_id` = VALUES(`budget_category_id`),
    `school_proximity` = VALUES(`school_proximity`),
    `hospital_proximity` = VALUES(`hospital_proximity`),
    `transit_proximity` = VALUES(`transit_proximity`),
    `in_house_laundry` = VALUES(`in_house_laundry`),
    `gym` = VALUES(`gym`),
    `pet_friendly` = VALUES(`pet_friendly`),
    `pool` = VALUES(`pool`),
    `is_logged_in` = VALUES(`is_logged_in`);
""")

# If user_id is None, use session_id to update the fields
update_preferences_user_id_query = text("""
UPDATE `tenant_preference_details`
SET
    `tenant_category_id` = :tenant_category_id,
    `location_category_id` = :location_category_id,
    `budget_category_id` = :budget_category_id,
    `school_proximity` = :school_proximity,
    `hospital_proximity` = :hospital_proximity,
    `transit_proximity` = :transit_proximity,
    `in_house_laundry` = :in_house_laundry,
    `gym` = :gym,
    `pet_friendly` = :pet_friendly,
    `pool` = :pool,
    `is_logged_in` = :is_logged_in
WHERE `user_id` = :user_id;
""")

def upsert_preferences_to_db(db: Session, data_dict: dict):
    """
    Data Access Layer function to save or update tenant preferences to the database.
    It performs an UPSERT query to insert or update the preferences.
    """
    
    # Extract the relevant keys and values dynamically, with user_id defaulting to None if not present
    params = {
        key: (data_dict.get("user_id") if key == "user_id" else data_dict.get(key))
        for key in [
            "user_id", "session_id", "tenant_category_id", "location_category_id", 
            "budget_category_id", "school_proximity", "hospital_proximity", 
            "transit_proximity", "in_house_laundry", "gym", "pet_friendly", 
            "pool", "is_logged_in"
        ]
    }
    
    if params.get("is_logged_in") is False:
        db.execute(upsert_preferences_session_id_query, params)  # Insert or update when user_id is None
    else:
        db.execute(update_preferences_user_id_query, params)  # Insert or update when user_id is provided
        
    db.commit()  # Commit the transaction to the database
   
    return True

#TODO: Call this query while login
def update_user_id_in_preference_table(db: Session, user_id: int, session_id: str, is_logged_in: bool):
    # Extract the relevant keys and values from the data_dict
    params = {
        "user_id": user_id,
        "session_id": session_id,
        "is_logged_in": is_logged_in
    }

    db.execute(update_user_id_query, params)
    db.commit()
    return True

update_user_id_query = text("""
UPDATE `tenant_preference_details`
SET `user_id` = :user_id,
    `is_logged_in` = :is_logged_in
WHERE `session_id` = :session_id;
""")