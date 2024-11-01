from sqlalchemy.orm import Session
from app.models.tenant import TenantPersonalDetails, TenantPropertyPreferences
from sqlalchemy import text
from app.global_constants import GET_LIKED_PROPERTIES_QUERY, GET_DISLIKED_PROPERTIES_QUERY

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
def create_property_preference(db: Session, preference: TenantPropertyPreferences):
    db.add(preference)
    db.commit()
    db.refresh(preference)
    return preference

def get_property_preference(db: Session, preference_id: int):
    """Retrieve property preference by ID."""
    return db.query(TenantPropertyPreferences).filter(TenantPropertyPreferences.id == preference_id).first()

def update_property_preference(db: Session, preference_id: int, is_liked: bool):
    """Update the 'is_liked' status of a property preference."""
    preference = db.query(TenantPropertyPreferences).filter(TenantPropertyPreferences.id == preference_id).first()
    if preference:
        preference.is_liked = is_liked
        db.commit()
    return preference

def delete_property_preference(db: Session, preference_id: int):
    """Delete a property preference by ID."""
    preference = db.query(TenantPropertyPreferences).filter(TenantPropertyPreferences.id == preference_id).first()
    if preference:
        db.delete(preference)
        db.commit()
    return preference

def get_preferences_by_user(db: Session, user_id: int):
    """Retrieve all property preferences for a specific user."""
    return db.query(TenantPropertyPreferences).filter(TenantPropertyPreferences.user_id == user_id).all()

def get_preferences_by_session(db: Session, session_id: str):
    """Retrieve all property preferences for a specific session."""
    return db.query(TenantPropertyPreferences).filter(TenantPropertyPreferences.session_id == session_id).all()

def get_liked_properties_for_user(db, user_id):
    return db.execute(text(GET_LIKED_PROPERTIES_QUERY), {"user_id": user_id}).fetchall()

def get_disliked_properties_for_user(db, user_id):
    return db.execute(text(GET_DISLIKED_PROPERTIES_QUERY), {"user_id": user_id}).fetchall()
