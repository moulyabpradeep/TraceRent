# tenant_service.py

from sqlalchemy.orm import Session
from app.data_access_objects.daos import UserPreferences
from app.dal.tenant_dal import (
    get_tenant, 
    create_tenant, 
    update_tenant, 
    delete_tenant, 
    get_all_tenants,
    get_tenant_by_email,
    get_tenants_by_province,
    create_property_preference,
    get_property_preference,
    update_property_preference,
    delete_property_preference,
    get_preferences_by_user,
    get_preferences_by_session,
    get_liked_properties_for_user,
    get_disliked_properties_for_user,
    save_tenant_preferences
)
from app.models.tenant import TenantPersonalDetails, TenantPreferenceDetails

def add_new_tenant(db: Session, tenant_data: dict):
    """Add a new tenant using provided data."""
    tenant = TenantPersonalDetails(**tenant_data)
    return create_tenant(db, tenant)

def get_tenant_by_id(db: Session, user_id: int):
    """Retrieve tenant details by user ID."""
    return get_tenant(db, user_id)

def update_existing_tenant(db: Session, user_id: int, tenant_update_data: dict):
    """Update a tenant's details by user ID."""
    return update_tenant(db, user_id, tenant_update_data)

def remove_tenant(db: Session, user_id: int):
    """Remove a tenant by user ID."""
    return delete_tenant(db, user_id)

def get_all_tenants_list(db: Session):
    """Retrieve all tenants."""
    return get_all_tenants(db)

def get_tenant_details_by_email(db: Session, email: str):
    """Retrieve tenant details by email."""
    return get_tenant_by_email(db, email)

def get_tenants_details_by_province(db: Session, province: str):
    """Retrieve tenants by province."""
    return get_tenants_by_province(db, province)

# Property Preferences Service Functions

def add_property_preference(db: Session, user_id: int, session_id: str, unit_id: int, is_liked: bool):
    """Add a new property preference for a user or session."""
    preference = TenantPreferenceDetails(user_id=user_id, session_id=session_id, unit_id=unit_id, is_liked=is_liked)
    return create_property_preference(db, preference)

def get_property_preference_details(db: Session, preference_id: int):
    """Retrieve property preference details by preference ID."""
    return get_property_preference(db, preference_id)

def get_all_preferences_by_user(db: Session, user_id: int):
    """Retrieve all property preferences for a specific user."""
    return get_preferences_by_user(db, user_id)

def get_all_preferences_by_session(db: Session, session_id: str):
    """Retrieve all property preferences for a specific session."""
    return get_preferences_by_session(db, session_id)

def save_preferences_to_db(db: Session, json_data: str):
    preferences = UserPreferences.from_json(json_data)
    return save_tenant_preferences(db, preferences)
