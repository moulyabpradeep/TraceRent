#tenant.py

from sqlalchemy import Column, Integer, String, Date
from app.database import Base
from app.global_constants import (  # Importing from constants
    TENANT_PERSONAL_DETAILS_TABLE,
    TENANT_PREFERENCE_DETAILS_TABLE,
    TENANT_CATEGORY_TABLE
)

class TenantPersonalDetails(Base):
    __tablename__ = TENANT_PERSONAL_DETAILS_TABLE  # Use constant for table name
    
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(Integer)
    province = Column(String)
    dob = Column(Date)

class TenantPreferenceDetails(Base):
    __tablename__ = TENANT_PREFERENCE_DETAILS_TABLE  # Use constant for table name
    
    user_id = Column(Integer, primary_key=True)
    tent_cat_id = Column(Integer)
    province = Column(String)
    country = Column(String)
    pets_preference = Column(String)
    family_with_kids = Column(String)
    amenities = Column(String)

class TenantCategory(Base):
    __tablename__ = TENANT_CATEGORY_TABLE  # Use constant for table name
    
    tent_cat_id = Column(Integer, primary_key=True)
    tent_category = Column(String)
