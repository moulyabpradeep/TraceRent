# tests/dal/test_tenant_dal.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import TenantPersonalDetails
from app.dal.tenant_dal import (
    get_tenant, create_tenant, update_tenant, delete_tenant,
    get_all_tenants, get_tenant_by_email, get_tenants_by_province
)
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get database connection URL
db_config = {
    'host': config['database']['host'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'database': config['database']['database']
}
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Database setup for testing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture for database session
@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

# Test cases

def test_create_tenant(db_session):
    new_tenant = TenantPersonalDetails(
        user_id=1,
        name="John Doe",
        email="johndoe@example.com",
        phone=1234567890,
        province="Ontario",
        dob="1990-01-01"
    )
    tenant = create_tenant(db_session, new_tenant)
    assert tenant.user_id == 1
    assert tenant.email == "johndoe@example.com"

def test_get_tenant(db_session):
    tenant = get_tenant(db_session, 1)
    assert tenant is not None
    assert tenant.user_id == 1

def test_update_tenant(db_session):
    tenant_update_data = {"name": "Jane Doe", "email": "janedoe@example.com"}
    tenant = update_tenant(db_session, user_id=1, tenant_update_data=tenant_update_data)
    assert tenant.name == "Jane Doe"
    assert tenant.email == "janedoe@example.com"

def test_delete_tenant(db_session):
    tenant = delete_tenant(db_session, user_id=1)
    assert tenant is not None
    assert get_tenant(db_session, 1) is None

def test_get_all_tenants(db_session):
    tenants = get_all_tenants(db_session)
    assert isinstance(tenants, list)

def test_get_tenant_by_email(db_session):
    tenant = get_tenant_by_email(db_session, "johndoe@example.com")
    assert tenant is not None
    assert tenant.email == "johndoe@example.com"

def test_get_tenants_by_province(db_session):
    tenants = get_tenants_by_province(db_session, "Ontario")
    assert len(tenants) > 0
