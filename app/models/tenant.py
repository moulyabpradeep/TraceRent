#tenant.py
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from app.database_connect import Base  # Assuming Base is already defined in your database connection module
from sqlalchemy.orm import relationship
from app.global_constants import (  # Importing from constants
    TENANT_PERSONAL_DETAILS_TABLE,
    TENANT_PREFERENCE_DETAILS_TABLE,
    TENANT_ACTIONS_TABLE,
    TENANT_CATEGORY_TABLE
)

class TenantPersonalDetails(Base):
    __tablename__ = TENANT_PERSONAL_DETAILS_TABLE  # Use constant for table name
    
    user_id = Column(Integer, primary_key=True)
    username=Column(String)
    password=Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(Integer)


class TenantPreferenceDetails(Base):
    __tablename__ = 'tenant_preference_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer, nullable=True)
    tenant_category_id = Column(Integer, ForeignKey('tenant_category.tent_cat_id'))
    location_category_id = Column(Integer)
    budget_category_id = Column(Integer)
    school_proximity = Column(Integer)
    hospital_proximity = Column(Integer)
    transit_proximity = Column(Integer)
    in_house_laundry = Column(Boolean, default=False)
    gym = Column(Boolean, default=False)
    pet_friendly = Column(Boolean, default=False)
    pool = Column(Boolean, default=False)
    is_logged_in = Column(Boolean, default=False)
    
     # Define relationships
    tenant_actions = relationship("TenantActions", back_populates="tenant_preference_details")

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "tenant_category_id": self.tenant_category_id,
            "location_category_id": self.location_category_id,
            "budget_category_id": self.budget_category_id,
            "school_proximity": self.school_proximity,
            "hospital_proximity": self.hospital_proximity,
            "transit_proximity": self.transit_proximity,
            "in_house_laundry": self.in_house_laundry,
            "gym": self.gym,
            "pet_friendly": self.pet_friendly,
            "pool": self.pool,
            "is_logged_in": self.is_logged_in,
            "tenant_actions": [action.to_dict() for action in self.tenant_actions]
        }


    @staticmethod
    def from_json(json_data: dict) -> 'TenantPreferenceDetails':
        # Use **json_data to unpack the dictionary directly into the model fields
        return TenantPreferenceDetails(**json_data)

class TenantCategory(Base):
    __tablename__ = TENANT_CATEGORY_TABLE  # Use constant for table name
    
    tent_cat_id = Column(Integer, primary_key=True)
    tent_category = Column(String)
