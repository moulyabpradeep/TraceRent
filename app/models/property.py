# property.py

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database_connect import Base
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship
from app.global_constants import (  # Importing from constants
    PROPERTY_CATEGORY_TABLE,
    TENANT_CATEGORY_TABLE,
    TENANT_PREFERRED_PROPERTIES_TABLE,
    PROPERTY_DATA_TABLE,
    PROP_CAT_ID_COLUMN,
    TENT_CAT_ID_COLUMN,
    TENANT_ACTIONS_TABLE
)

class TenantPreferredProperties(Base):
    __tablename__ = TENANT_PREFERRED_PROPERTIES_TABLE  # Use constant for table name
    
    id = Column(Integer, primary_key=True)
    tent_cat_id = Column(Integer, ForeignKey(f'{TENANT_CATEGORY_TABLE}.{TENT_CAT_ID_COLUMN}'))  # Using constant for ForeignKey
    prop_cat_id = Column(Integer, ForeignKey(f'{PROPERTY_CATEGORY_TABLE}.{PROP_CAT_ID_COLUMN}'))  # Using constant for ForeignKey

# PropertyData Model
class PropertyData(Base):
    __tablename__ = PROPERTY_DATA_TABLE  # Use constant for table name

    unit_id = Column(Integer, primary_key=True, index=True)
    unit_number = Column(Integer)
    prop_cat_id = Column(Integer, ForeignKey(f'{PROPERTY_CATEGORY_TABLE}.{PROP_CAT_ID_COLUMN}'))  # Using constant for ForeignKey
    prop_name = Column(String(255))
    prop_type = Column(String(255))
    no_of_rooms = Column(String(255))
    area_code = Column(String(255))
    province = Column(String(255))
    country = Column(String(255))
    address = Column(String(255))
    rent = Column(Numeric(10, 2))
    lease_length = Column(String(255))

    # Relationships
    property_category = relationship("PropertyCategory", back_populates="property_data")
    property_media = relationship("PropertyMedia", back_populates="property_data")
    location = relationship("Location", back_populates="property_data")
    amenities = relationship("Amenities", back_populates="property_data")
    tenant_actions = relationship("TenantActions", back_populates="property_data")

    def to_dict(self):
        return {
            "unit_id": self.unit_id,
            "unit_number": self.unit_number,
            "prop_name": self.prop_name,
            "prop_type": self.prop_type,
            "no_of_rooms": self.no_of_rooms,
            "area_code": self.area_code,
            "province": self.province,
            "country": self.country,
            "address": self.address,
            "rent": str(self.rent),
            "lease_length": self.lease_length,
            "property_category": {
                "prop_cat_id": self.property_category.prop_cat_id,
                "prop_category": self.property_category.prop_category
            },
            "property_media": [media.to_dict() for media in self.property_media],
            "location": [location.to_dict() for location in self.location],
            "amenities": [amenities.to_dict() for amenities in self.amenities],
            "tenant_actions": [tenant_action.to_dict() for tenant_action in self.tenant_actions]
        }

# PropertyCategory Model
class PropertyCategory(Base):
    __tablename__ = PROPERTY_CATEGORY_TABLE

    prop_cat_id = Column(Integer, primary_key=True, index=True)
    prop_category = Column(String(255))

    # Relationship back_populates
    property_data = relationship("PropertyData", back_populates="property_category")

    def to_dict(self):
        return {
            "prop_cat_id": self.prop_cat_id,
            "prop_category": self.prop_category
        }

# PropertyMedia Model
class PropertyMedia(Base):
    __tablename__ = 'property_media'

    media_id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey('property_data.unit_id'))
    category = Column(String(255))
    photo_url = Column(String(255))
    sequence = Column(Integer)

    # Relationship back_populates
    property_data = relationship("PropertyData", back_populates="property_media")

    def to_dict(self):
        return {
            "media_id": self.media_id,
            "category": self.category,
            "photo_url": self.photo_url,
            "sequence": self.sequence
        }

# Location Model
class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey('property_data.unit_id'))
    apt_unit_number = Column(String(50))
    street_name = Column(String(255))
    community = Column(String(255))
    city = Column(String(255))
    province = Column(String(255))
    country = Column(String(255))
    latitude = Column(String(50))
    longitude = Column(String(50))

    # Relationship back_populates
    property_data = relationship("PropertyData", back_populates="location")

    def to_dict(self):
        return {
            "apt_unit_number": self.apt_unit_number,
            "street_name": self.street_name,
            "community": self.community,
            "city": self.city,
            "province": self.province,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

# Amenities Model
class Amenities(Base):
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey('property_data.unit_id'))
    accessibility = Column(String(255))
    parking = Column(Integer)
    gym = Column(Boolean)
    kids_playarea = Column(Boolean)
    party_hall = Column(Boolean)
    backyard = Column(Boolean)
    deck = Column(Boolean)
    in_house_laundry = Column(Boolean)
    visitor_parking = Column(Boolean)
    pool = Column(Boolean)
    pet_friendly = Column(Boolean)

    # Relationship back_populates
    property_data = relationship("PropertyData", back_populates="amenities")

    def to_dict(self):
        return {
            "accessibility": self.accessibility,
            "parking": self.parking,
            "gym": self.gym,
            "kids_playarea": self.kids_playarea,
            "party_hall": self.party_hall,
            "backyard": self.backyard,
            "deck": self.deck,
            "in_house_laundry": self.in_house_laundry,
            "visitor_parking": self.visitor_parking,
            "pool": self.pool,
            "pet_friendly": self.pet_friendly
        }

# TenantActions Model
class TenantActions(Base):
    __tablename__ = TENANT_ACTIONS_TABLE

    action_id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_preference_details_id = Column(Integer, ForeignKey('tenant_preference_details.id'))
    unit_id = Column(Integer, ForeignKey('property_data.unit_id', ondelete='CASCADE'))
    is_liked = Column(Boolean, default=None)
    is_contacted = Column(Boolean, default=None)

    # Relationships
    tenant_preference_details = relationship("TenantPreferenceDetails", back_populates="tenant_actions")
    property_data = relationship("PropertyData", back_populates="tenant_actions")

    def to_dict(self):
        return {
            "action_id": self.action_id,
            "tenant_preference_details_id": self.tenant_preference_details_id,
            "unit_id": self.unit_id,
            "is_liked": self.is_liked,
            "is_contacted": self.is_contacted
        }
