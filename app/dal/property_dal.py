# property_dal.py

from sqlalchemy.orm import Session
from app.models.property import PropertyData, TenantPreferredProperties
from sqlalchemy import func

# CRUD for property_data
def get_property(db: Session, unit_id: int):
    """Retrieve property details by unit ID."""
    return db.query(PropertyData).filter(PropertyData.unit_id == unit_id).first()

def create_property(db: Session, property_data: PropertyData):
    """Create a new property record."""
    db.add(property_data)
    db.commit()
    db.refresh(property_data)
    return property_data

def update_property(db: Session, unit_id: int, property_update_data: dict):
    """Update a property by unit ID."""
    property_ = db.query(PropertyData).filter(PropertyData.unit_id == unit_id).first()
    if property_:
        for key, value in property_update_data.items():
            setattr(property_, key, value)
        db.commit()
    return property_

def get_all_properties(db: Session):
    """Retrieve all properties."""
    return db.query(PropertyData).all()



# Get minimum and maximum rent for a given tenant category in a single call
def get_price_range_for_tenant_category(db: Session, tenant_category_id: int):
    min_rent, max_rent = (
        db.query(func.min(PropertyData.rent), func.max(PropertyData.rent))
        .join(
            TenantPreferredProperties,
            TenantPreferredProperties.prop_cat_id == PropertyData.prop_cat_id
        )
        .filter(TenantPreferredProperties.tent_cat_id == tenant_category_id)
        .first()
    )
    return min_rent, max_rent
