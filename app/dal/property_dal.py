# property_dal.py

from sqlalchemy.orm import Session
from app.models.property import PropertyData

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

def delete_property(db: Session, unit_id: int):
    """Delete a property by unit ID."""
    property_ = db.query(PropertyData).filter(PropertyData.unit_id == unit_id).first()
    if property_:
        db.delete(property_)
        db.commit()
    return property_

def get_all_properties(db: Session):
    """Retrieve all properties."""
    return db.query(PropertyData).all()
