# tenant_dal.py

from sqlalchemy.orm import Session
from app.models.tenant import TenantPersonalDetails, TenantPreferenceDetails
from data_access_objects.daos import UserPreferences
from dataclasses import asdict
from sqlalchemy import text
from db_queries import (
    UPSERT_TENANT_PREFERENCES,
    GET_LIKED_PROPERTIES_QUERY,
    GET_DISLIKED_PROPERTIES_QUERY
)

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

def save_tenant_preferences(db, preferences: UserPreferences):
    try:
        # Convert the dataclass to a dictionary
        params = asdict(preferences)
        
        # Adjust user_id to be None if it’s empty
        if not params["user_id"]:
            params["user_id"] = None
        
        # Execute the UPSERT query
        db.execute(text(UPSERT_TENANT_PREFERENCES), params)
        db.commit()  # Commit the transaction to save the changes
        
        return True  # Return True if save was successful
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        print(f"Error saving preferences: {e}")
        return False  # Return False if there was an error

