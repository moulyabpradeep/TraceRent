from sqlalchemy.orm import Session
from app.database_connect import SessionLocal
from app.models.tenant import TenantCategory, TenantPreferredProperties
from app.models.property import PropertyCategory
from app.data_access_objects.data_cache import DataCache  # Ensure correct imports

def load_static_data(db: Session):
    # Get the singleton instance of DataCache
    cache = DataCache()
    
    # Load tenant categories
    cache.tenant_categories = db.query(TenantCategory).all()
    
    # Load property categories
    cache.property_categories = db.query(PropertyCategory).all()
    
    # Load tenant preferred properties
    cache.tenant_preferred_properties = db.query(TenantPreferredProperties).all()
    
    print("Static data loaded into cache.")
