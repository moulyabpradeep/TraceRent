# property_service.py

from sqlalchemy.orm import Session
from app.dal.property_dal import get_property, create_property, update_property, delete_property, get_all_properties
from app.models.property import PropertyData, TenantPreferredProperties

def add_new_property(db: Session, property_data: dict):
    """Add a new property using provided data."""
    property_ = PropertyData(**property_data)
    return create_property(db, property_)

def get_property_by_id(db: Session, unit_id: int):
    """Retrieve property details by unit ID."""
    return get_property(db, unit_id)

def update_existing_property(db: Session, unit_id: int, property_update_data: dict):
    """Update a property's details by unit ID."""
    return update_property(db, unit_id, property_update_data)

def remove_property(db: Session, unit_id: int):
    """Remove a property by unit ID."""
    return delete_property(db, unit_id)

def get_all_properties_list(db: Session):
    """Retrieve all properties."""
    return get_all_properties(db)

def get_properties_by_category(db: Session, category_id: int):
    """Retrieve properties by category ID."""
    return db.query(PropertyData).filter(PropertyData.prop_cat_id == category_id).all()

def get_tenant_preferred_properties(db: Session, tenant_category_id: int):
    """Retrieve properties preferred by a tenant category."""
    return db.query(TenantPreferredProperties).filter(TenantPreferredProperties.tent_cat_id == tenant_category_id).all()
