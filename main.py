from flask import Flask, request, jsonify
import configparser
import json
from app.DataAccessObjects.DAOs import PropertyObject
from app.business import TenantMatchingIMPL as impl
from app.routes import TraceRentAPIInvoker as api
import os
from app.routes import TraceRentAPIInvoker as tcapi
from app.DataAccessObjects import DAOs

app = Flask(__name__)


# Load properties from a configuration file
def load_properties(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


# Tenant Matching function
def tenantMatching(customer_preferences):
    rangeFound = False
    final_list = None
    bucket_list = None
    tenant_category_id = customer_preferences.tenant_category_id
    budget_category_id = customer_preferences.budget_category_id
    city = customer_preferences.city

    # Load properties
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), './config.ini'))

    # Accessing properties using the section names
    priceRange = None#impl.get_price_range(tenant_category_id)
    data = None#api.search_properties(customer_preferences, priceRange.index(budget_category_id-1))

    # Sample data (for testing)
    data = [
    PropertyObject(
        property_price=1500,
        property_coordinates=(42.333, -43.67),
        school_proximity=5,
        hospital_proximity=3,
        transit_proximity=4,
        in_house_laundry=True,
        gym=True,
        pet_friendly=False,
        pool=True,
    ),
    PropertyObject(
        property_price=1200,
        property_coordinates=(52.333, -53.67),
        school_proximity=2,
        hospital_proximity=4,
        transit_proximity=5,
        in_house_laundry=False,
        gym=True,
        pet_friendly=True,
        pool=False,
        points=78,
        percent_close=80
    ),
    PropertyObject(
        property_price=2000,
        property_coordinates=(82.333, -93.67),
        school_proximity=1,
        hospital_proximity=2,
        transit_proximity=3,
        in_house_laundry=True,
        gym=False,
        pet_friendly=True,
        pool=True,
        points=92,
        percent_close=95
    ),
    PropertyObject(
        property_price=1000,
        property_coordinates=(72.333, -33.67),
        school_proximity=3,
        hospital_proximity=5,
        transit_proximity=2,
        in_house_laundry=False,
        gym=False,
        pet_friendly=False,
        pool=False,
        points=65,
        percent_close=75
    ),
    PropertyObject(
        property_price=1800,
        property_coordinates=(32.333, -33.67),
        school_proximity=4,
        hospital_proximity=4,
        transit_proximity=5,
        in_house_laundry=True,
        gym=True,
        pet_friendly=True,
        pool=True,
        points=88,
        percent_close=85
    ),
    ]

    if not data:
        return None

    maxPoints = impl.getMaxPoints(customer_preferences)
    sorted_property_list = impl.assign_and_sort_property_list(data, customer_preferences, city)
    final_list = impl.add_percent_close(sorted_property_list, maxPoints)
    bucket_list == impl.categorize_properties_by_percent_close(final_list)
    return bucket_list


# Define the route to access tenantMatching method
@app.route('/tenantMatching', methods=['GET'])
def tenant_matching_api():
    customer_preferences = DAOs.UserPreferences.from_json(request.json)
    result = tenantMatching(customer_preferences)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"error": "No properties found"}), 404


# Empty method for getting price range
@app.route('/priceRange', methods=['GET'])
def get_price_range_api():
    # TODO: Implement the logic to fetch the price range
    return jsonify({"message": "Price range fetching logic not implemented"}), 200


# Empty method for saving customer preferences
@app.route('/savePreferences', methods=['POST'])
def save_preferences_api():
    preferences = DAOs.UserPreferences.from_json(request.json)
    return tcapi.save_preferences_to_db(preferences)


# Method for signing up
@app.route('/signup', methods=['POST'])
def sign_up_api():
    user_data = DAOs.UserData.from_json(request.json)
    return tcapi.sign_up_api(user_data)


# Method for logging in
@app.route('/login', methods=['POST'])
def login_api():
    user_data = DAOs.UserData.from_json(request.json)
    return tcapi.login_api(user_data)


#uncomment for api testing
#if __name__ == '__main__':
#    app.run(debug=True)


#uncomment for local testing

def tenant_matching_api_local():
    # JSON data as a string
    user_preferences_json = '''{
        "user_id": "user123",
        "tenant_category_id": 1,
        "location_category_id": 2,
        "budget_category_id": 3,
        "school_proximity": 5,
        "hospital_proximity": 5,
        "transit_proximity": 5,
        "in_house_laundry": true,
        "gym": false,
        "pet_friendly": true,
        "pool": false,
        "is_logged_in": true,
        "session_id": "LattafaAlNashamaCaprice"
    }'''

    # Using the JSON string directly for from_json method
    customer_preferences = DAOs.UserPreferences.from_json(user_preferences_json)
    result = tenantMatching(customer_preferences)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"error": "No properties found"}), 404


login_request = {
    "user_email": "john.doe@example.com",
    "user_password": "SecurePassword123",
    "sessionId": "abc123session"
}
tenant_matching_api_local()