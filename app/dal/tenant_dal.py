# tenant_dal.py

from sqlalchemy.orm import Session
from app.models.tenant import TenantPersonalDetails

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
