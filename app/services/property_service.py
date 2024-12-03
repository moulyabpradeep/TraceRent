# property_service.py

from sqlalchemy.orm import Session
from app.database_connect import SessionLocal
from app.dal.property_dal import *
from app.models.property import PropertyData
from app.models.tenant import TenantPreferredProperties
from app.data_access_objects.daos import TenantActionFilterType
from app.data_access_objects.data_cache import DataCache
from sqlalchemy import and_


def add_new_property(db: Session, property_data: dict):
    """Add a new property using provided data."""
    property_ = PropertyData(**property_data)
    return create_property(db, property_)

def update_existing_property(db: Session, unit_id: int, property_update_data: dict):
    """Update a property's details by unit ID."""
    return update_property(db, unit_id, property_update_data)


def get_all_properties_list(db: Session):
    """Retrieve all properties."""
    return get_all_properties(db)

def get_properties_by_category(db: Session, category_id: int):
    """Retrieve properties by category ID."""
    return db.query(PropertyData).filter(PropertyData.prop_cat_id == category_id).all()


def get_all_properties_on_tenant_budget_category(tenant_cat_id: int, min_rent: float, max_rent: float, city:str):
    # Initialize the database session
    db = SessionLocal()
    
    # Access the cache
    cache = DataCache()
    # Fetch preferred property categories for the specified tenant category ID
    preferred_properties = cache.get_preferred_properties(tenant_cat_id)
    print(f"The preferred_properties  are: {preferred_properties} and city: {city}")
    try:
        # Query PropertyData with preferred property categories and rent range filters
        results = db.query(PropertyData).join(Location).options(
            joinedload(PropertyData.location),  # Eager load location
            joinedload(PropertyData.amenities),
            subqueryload(PropertyData.property_media)  # Eager load PropertyMedia (one-to-many)
        ).filter(
            and_(
                PropertyData.prop_cat_id.in_(preferred_properties),
                Location.city == city,  # Use Location.city to filter by city
                PropertyData.rent >= min_rent,
                PropertyData.rent <= max_rent
            )
        ).all()
   
        # Flatten each property using the to_flat_dict method
        response = [property.to_flat_dict() for property in results]

    except Exception as e:
        # Optional: Log or handle the error as needed
        print(f"Error fetching properties: {e}")
        response = []

    finally:
        # Close the database session
        db.close()
    
    return response


def get_tenant_preferred_properties(db: Session, tenant_category_id: int):
    """Retrieve properties preferred by a tenant category."""
    return db.query(TenantPreferredProperties).filter(TenantPreferredProperties.tent_cat_id == tenant_category_id).all()

def get_price_range(city: String, tenant_category_id: int):
    db = SessionLocal()
    
    try:
        return get_price_range_for_tenant_category(db, tenant_category_id)
        # return {"min_rent": min_rent, "max_rent": max_rent}
    finally:
        db.close()

def get_property_data(unit_id: int):
    # Initialize the database session
    db = SessionLocal()
    
    try:
        # Fetch property data by unit_id
        property_data = get_property_data_by_unit_id(db, unit_id)

        # Check if no property was found
        if not property_data:
            return {"message": "Property not found"}

        # Use the to_dict() method to serialize the property data
        response = property_data.to_dict()
        
    finally:
        # Close the database session
        db.close()
    
    return response

def get_properties_data(unit_ids: list):
    # Initialize the database session
    db = SessionLocal()

    # Fetch properties in bulk using the optimized DAL function
    properties_data = get_all_properties_by_unit_ids(db, unit_ids)

    # Close the database session
    db.close()

    # Check if no properties were found
    if not properties_data:
        return {"message": "Properties not found"}

    # Use the to_dict() method to serialize each property and return as a list
    response = [property_data.to_dict() for property_data in properties_data]
    
    return response


def get_properties_by_action(user_id:int, filter_type:TenantActionFilterType):
    # Initialize the database session
    db = SessionLocal()
    print(user_id, filter_type)
    
    # Fetch properties in bulk using the optimized DAL function
    properties_data = get_properties_by_tenant_action_filter(db, user_id, filter_type)
    
    # Close the database session
    db.close()

    # Check if no properties were found
    if not properties_data:
        return {"message": "Properties not found"}

    # Use the to_dict() method to serialize each property and return as a list
    response = [property_data for property_data in properties_data]

    return response



def get_property_details(unit_id:int):
    # Initialize the database session
    db = SessionLocal()
    print(unit_id)
    
    # Fetch properties in bulk using the optimized DAL function
    property_data = get_property_by_unit_id(db, unit_id)
    
    # Close the database session
    db.close()

    # Check if no properties were found
    if not property_data:
        return {"message": "Property not found"}

    # Use the to_dict() method to serialize each property and return as a list

    return property_data




def get_property_owner_info(unit_id:int):
    # Initialize the database session
    db = SessionLocal()
    print(unit_id)
    
    # Fetch properties in bulk using the optimized DAL function
    property_owner_info = get_property_owner(db, unit_id)
    
    # Close the database session
    db.close()

    # Check if no properties were found
    if not property_owner_info:
        return {"message": "Property not found"}

    # Use the to_dict() method to serialize each property and return as a list

    return property_owner_info
