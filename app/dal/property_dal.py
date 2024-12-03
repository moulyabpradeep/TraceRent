# property_dal.py

from sqlalchemy.orm import Session
from app.models.property import *
from app.models.tenant import TenantPreferenceDetails, TenantActions, TenantPreferredProperties
from sqlalchemy import func
from app.data_access_objects.daos import TenantActionFilterType
from sqlalchemy.orm import joinedload, subqueryload

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




def get_properties_by_tenant_action_filter(db, user_id,session_id, filter_type: TenantActionFilterType):
    # Initialize the base query
    query = db.query(TenantPreferenceDetails).options(
        # Eager load tenant_actions and its relationships
        joinedload(TenantPreferenceDetails.tenant_actions)
        .joinedload(TenantActions.property_data)
        .options(
            joinedload(PropertyData.location),  # Eager load Location (one-to-one)
            joinedload(PropertyData.amenities),  # Eager load Amenities (one-to-one)
            joinedload(PropertyData.property_owner_info),  # Eager load PropertyOwnerInfo (one-to-one)
            subqueryload(PropertyData.property_media)  # Eager load PropertyMedia (one-to-many)
        )
    )

    # Apply filter for user_id or session_id
    if user_id:
        query = query.filter(TenantPreferenceDetails.user_id == user_id)
    elif session_id:
        query = query.filter(TenantPreferenceDetails.session_id == session_id)
    else:
        raise ValueError("Either user_id or session_id must be provided.")

    # Apply the dynamic filter based on filter_type
    if filter_type:
        filter_type = filter_type.upper()
        if filter_type == "LIKED":
            query = query.filter(TenantActions.is_liked == True)  # Filter for liked properties
        elif filter_type == "DISLIKED":
            query = query.filter(TenantActions.is_liked == False)  # Filter for disliked properties
        elif filter_type == "CONTACTED":
            query = query.filter(TenantActions.is_contacted == True)  # Filter for contacted properties

    # Execute the query and fetch results
    tenant_preferences = query.all()

    # Convert results to dictionary format
    response = [tpd.to_dict() for tpd in tenant_preferences]
    return response


def get_property_by_unit_id(db, unit_id: int) -> dict:
    # Initialize the query
    property_data = db.query(PropertyData).options(
        joinedload(PropertyData.location),  # Eager load Location (one-to-one)
        joinedload(PropertyData.amenities),  # Eager load Amenities (one-to-one)
        joinedload(PropertyData.property_owner_info),  # Eager load propertyOwnerInfo (one-to-one)
        subqueryload(PropertyData.property_media)  # Eager load PropertyMedia (one-to-many)
    ).filter(PropertyData.unit_id == unit_id).first()

    # Check if property_data exists to avoid AttributeError
    if not property_data:
        return None  # or an empty dictionary {}, or handle it as needed

    # Convert results to dictionary format
    response = property_data.to_dict()
    return response



def get_property_owner(db, unit_id: int) -> dict:
    # Initialize the query
    property_owner = db.query(PropertyOwnerInfo).filter(PropertyOwnerInfo.unit_id == unit_id).first()

    # Check if property_data exists to avoid AttributeError
    if not property_owner:
        return None  # or an empty dictionary {}, or handle it as needed

    # Convert results to dictionary format
    response = property_owner.to_dict()
    return response