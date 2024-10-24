# tenant_service.py

from sqlalchemy.orm import Session
from app.dal.tenant_dal import get_tenant, create_tenant, update_tenant, delete_tenant, get_all_tenants
from app.models.tenant import TenantPersonalDetails

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

def get_tenant_by_email(db: Session, email: str):
    """Retrieve tenant details by email."""
    return db.query(TenantPersonalDetails).filter(TenantPersonalDetails.email == email).first()

def get_tenants_by_province(db: Session, province: str):
    """Retrieve tenants by province."""
    return db.query(TenantPersonalDetails).filter(TenantPersonalDetails.province == province).all()
