import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from app.data_access_objects.daos import UserPreferences
from app.services.tenant_service import save_preferences_to_db
from app.dal import tenant_dal

@pytest.fixture
def mock_db_session():
    # Create a mock database session
    return MagicMock(spec=Session)

@pytest.fixture
def json_data():
    # Example JSON data that would represent user preferences
    return '{"user_id":1,"tenant_category_id":1,"location_category_id":1,"budget_category_id":1,"school_proximity":1,"hospital_proximity":2,"transit_proximity":5,"in_house_laundry":false,"gym":false,"pet_friendly":false,"pool":false,"is_logged_in":false,"session_id":1}'

def test_save_preferences_to_db(mock_db_session, json_data):
    # Mock the response of the save_tenant_preferences function in tenant_dal
    preferences_mock = MagicMock(spec=UserPreferences)
    tenant_dal.save_tenant_preferences = MagicMock(return_value=preferences_mock)

    # Call the function with the mocked DB session and JSON data
    result = save_preferences_to_db(mock_db_session, json_data)

    # Assertions
    tenant_dal.save_tenant_preferences.assert_called_once_with(mock_db_session, preferences_mock)
    assert result == preferences_mock  # Check if the function returns the correct object

    # Verify the UserPreferences is created correctly from the JSON
    preferences_mock.from_json.assert_called_once_with(json_data)
