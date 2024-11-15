# tenant_service.py

from sqlalchemy.orm import Session
from app.dal.tenant_dal import *
from app.models.tenant import *
from app.database_connect import SessionLocal
from app.data_access_objects.daos import TenantActionsData


def add_new_tenant(tenant_data: dict):
    """Add a new tenant using provided data."""
    tenant = TenantPersonalDetails(**tenant_data)
    db = SessionLocal()
    
    try:
        return  create_tenant(db, tenant)
    finally:
        db.close()

def get_tenant_by_id(user_id: int):
    """Retrieve tenant details by user ID."""
    db = SessionLocal()
    
    try:
        return  get_tenant(db, user_id)
    finally:
        db.close()

def update_existing_tenant(user_id: int, tenant_update_data: dict):
    """Update a tenant's details by user ID."""
    db = SessionLocal()
    
    try:
        return  update_tenant(db, user_id, tenant_update_data)
    finally:
        db.close()

def remove_tenant(user_id: int):
    """Remove a tenant by user ID."""
    db = SessionLocal()
    
    try:
        return  delete_tenant(db, user_id)
    finally:
        db.close()

def get_all_tenants_list(db: Session):
    """Retrieve all tenants."""
    db = SessionLocal()
    
    try:
        return  get_all_tenants(db)
    finally:
        db.close()

def get_tenant_details_by_email(email: str):
    """Retrieve tenant details by email."""
    db = SessionLocal()
    
    try:
        return  get_tenant_by_email(db, email)
    finally:
        db.close()

def get_tenants_details_by_province(province: str):
    """Retrieve tenants by province."""
    db = SessionLocal()
    
    try:
        return  get_tenants_by_province(db, province)
    finally:
        db.close()

# Property Preferences Service Functions

def add_property_preference(user_id: int, session_id: str, unit_id: int, is_liked: bool):
    """Add a new property preference for a user or session."""
    preference = TenantPreferenceDetails(user_id=user_id, session_id=session_id, unit_id=unit_id, is_liked=is_liked)
    db = SessionLocal()
    
    try:
        return  create_property_preference(db, preference)
    finally:
        db.close()

def get_property_preference_details(preference_id: int):
    """Retrieve property preference details by preference ID."""
    db = SessionLocal()
    
    try:
        return  get_property_preference(db, preference_id)
    finally:
        db.close()

def get_all_preferences_by_user(user_id: int):
    """Retrieve all property preferences for a specific user."""
    db = SessionLocal()
    
    try:
        return  get_preferences_by_user(db, user_id)
    finally:
        db.close()

def get_all_preferences_by_session(session_id: str):
    """Retrieve all property preferences for a specific session."""
    db = SessionLocal()
    
    try:
        return  get_preferences_by_session(db, session_id)
    finally:
        db.close()


def save_preferences_service(json_data):
    """
    Service function to save or update tenant preferences.
    It calls the DAL to interact with the database.
    """
    db = SessionLocal()
    try:
        return  upsert_preferences_to_db(db, json_data)
    finally:
        db.close()
        

def update_user_id_in_preferences(user_id: int, session_id: str, is_logged_in: bool):
    """
    Service function to update tenant preferences with user-id and is-logged-in
    """
    db = SessionLocal()
    try:
        return  update_user_id_in_preference_table(db, user_id, session_id, is_logged_in)
    
    finally:
        db.close()


def handle_tenant_actions(json_data) -> bool:
    # Convert JSON to TenantActionsData object using the static method
    tenant_action_data = TenantActionsData.from_json(json_data)
    
    session = SessionLocal()
    try:
        return upsert_tenant_action(session, tenant_action_data)
    finally:
        session.close()
