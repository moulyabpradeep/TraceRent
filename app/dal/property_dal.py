# property_dal.py

from sqlalchemy.orm import Session
from app.models.property import PropertyData, TenantPreferredProperties
from sqlalchemy import func

# CRUD for property_data

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


# Function to fetch property data based on unit_id
def get_property_data_by_unit_id(db: Session, unit_id: int):

    try:
        # Fetch property data with related tables
        property_data = db.query(PropertyData).filter(PropertyData.unit_id == unit_id).first()

        return property_data  # Return the model instance

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the session
        db.close()

def get_all_properties_by_unit_ids(db: Session,unit_ids: list):
    # Fetch all property data for the given list of unit_ids using a single query
    try:
        # Fetch properties data with related tables
        properties = db.query(PropertyData).filter(PropertyData.unit_id.in_(unit_ids)).all()
        return properties  # Return the model instance

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        # Close the session
        db.close()
