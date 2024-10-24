# property.py

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from app.global_constants import (  # Importing from constants
    PROPERTY_CATEGORY_TABLE,
    TENANT_CATEGORY_TABLE,
    TENANT_PREFERRED_PROPERTIES_TABLE,
    PROPERTY_DATA_TABLE,
    PROP_CAT_ID_COLUMN,
    TENT_CAT_ID_COLUMN
)

class PropertyCategory(Base):
    __tablename__ = PROPERTY_CATEGORY_TABLE  # Use constant for table name
    
    prop_cat_id = Column(Integer, primary_key=True)
    prop_category = Column(String)

class TenantPreferredProperties(Base):
    __tablename__ = TENANT_PREFERRED_PROPERTIES_TABLE  # Use constant for table name
    
    id = Column(Integer, primary_key=True)
    tent_cat_id = Column(Integer, ForeignKey(f'{TENANT_CATEGORY_TABLE}.{TENT_CAT_ID_COLUMN}'))  # Using constant for ForeignKey
    prop_cat_id = Column(Integer, ForeignKey(f'{PROPERTY_CATEGORY_TABLE}.{PROP_CAT_ID_COLUMN}'))  # Using constant for ForeignKey

class PropertyData(Base):
    __tablename__ = PROPERTY_DATA_TABLE  # Use constant for table name
    
    prop_cat_id = Column(Integer, ForeignKey(f'{PROPERTY_CATEGORY_TABLE}.{PROP_CAT_ID_COLUMN}'))  # Using constant for ForeignKey
    unit_id = Column(Integer, primary_key=True)
    prop_name = Column(String)
    prop_type = Column(String)
    no_of_rooms = Column(String)
