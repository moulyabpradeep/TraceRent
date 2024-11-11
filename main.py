from flask import Flask, request, jsonify, abort
from functools import wraps
import configparser
import json
from app.DataAccessObjects.DAOs import PropertyObject
from app.business import TenantMatchingIMPL as impl
from app.routes import TraceRentAPIInvoker as api
import os
from pathlib import Path
from app.routes import TraceRentAPIInvoker as tcapi
from app.DataAccessObjects import DAOs
import base64
from app.services.tenant_service import *
from app.services.user_service import *
from mysql.connector import Error


app = Flask(__name__)


def check_auth(username, password):
    """Verify if the provided username and password are correct."""
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent / 'config.ini'

    config.read(config_path)
    auth_user = config.get('authentication', 'user')
    auth_password = config.get('authentication', 'password')

    return username == auth_user and password == auth_password


def require_basic_auth(f):
    """Decorator to enforce basic authentication."""

    @wraps(f)
    def decorated(*args, **kwargs):
        if (request is None) or (request.headers is None) or ('Authorization' not in request.headers):
            return jsonify({"error": "Invalid credentials."}), 401
        authFromUser = request.headers.get("Authorization")
        if not authFromUser or not authFromUser.startswith("Basic "):
            # Abort with 401 if no credentials are provided
            return jsonify({"error": "Authentication required."}), 401

        # Decode base64 encoded credentials
        try:
            base64_credentials = authFromUser.split(" ")[1]
            credentials = base64.b64decode(base64_credentials).decode("utf-8")
            username, password = credentials.split(":")
        except Exception as e:
            return jsonify({"error": "Invalid authentication header."}), 401

        # Check if credentials are correct
        if not check_auth(username, password):
            return jsonify({"error": "Invalid credentials."}), 401

        return f(*args, **kwargs)

    return decorated


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
        property_coordinates=(49.6945782, -112.8331033),
        school_proximity=2,
        hospital_proximity=4,
        transit_proximity=5,
        in_house_laundry=False,
        gym=True,
        pet_friendly=True,
        pool=False
    ),
    PropertyObject(
        property_price=2000,
        property_coordinates=(82.333, -93.67),
        school_proximity=1000000000,
        hospital_proximity=2000000,
        transit_proximity=3000000,
        in_house_laundry=True,
        gym=False,
        pet_friendly=True,
        pool=True
    ),
    PropertyObject(
        property_price=1000,
        property_coordinates=(72.333, -33.67),
        school_proximity=30000,
        hospital_proximity=50000,
        transit_proximity=20000,
        in_house_laundry=False,
        gym=False,
        pet_friendly=False,
        pool=False
    ),
    PropertyObject(
        property_price=1800,
        property_coordinates=(32.333, -33.67),
        school_proximity=400,
        hospital_proximity=4000,
        transit_proximity=50000,
        in_house_laundry=True,
        gym=True,
        pet_friendly=True,
        pool=True,
    ),
    ]

    if not data:
        return None

    max_points = impl.getMaxPoints(customer_preferences)
    print("MAX POINTS: " + str(max_points))

    sorted_property_list = impl.assign_and_sort_property_list(data, customer_preferences, city, max_points)

    for property_obj in sorted_property_list:
        print(f"Property Price: {str(property_obj.property_price)}, Points: {str(property_obj.points)}")

    final_list = impl.add_percent_close(sorted_property_list, max_points)

    bucket_list = impl.categorize_properties_by_percent_close(final_list)

    return bucket_list


# Define the route to access tenantMatching method
@app.route('/tenantMatching', methods=['GET'])
@require_basic_auth
def tenant_matching_api():
    # Get the JSON request body as a dictionary
    requestJSON = request.json

    # Parse the JSON into a UserPreferences object
    customer_preferences = DAOs.UserPreferences.from_json(requestJSON)
    result = tenantMatching(customer_preferences)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"error": "No properties found"}), 404


# Empty method for getting price range
@app.route('/priceRange', methods=['GET'])
@require_basic_auth
def get_price_range_api():
    # TODO: Implement the logic to fetch the price range
    return jsonify({"message": "Price range fetching logic not implemented"}), 200

"""
# Method for saving customer preferences : WORKING PERFECTLY FINE
@app.route('/savePreferences', methods=['POST'])
@require_basic_auth
def save_preferences_api():
    #preferences = DAOs.UserPreferences.from_json(request.json)
    try:
        print(request.json)
        
        if(save_preferences_service(request.json)):
            print("Preferences successfully saved to the database.")
            return jsonify({"message": "Preferences saved successfully!"}), 201
        else:
            return jsonify({"message": "Something went wrong!"}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": "Something went wrong"}), 500
"""

# Method for saving customer preferences
@app.route('/savePreferences', methods=['POST'])
@require_basic_auth
def save_preferences_api():
    try:
        print(request.json)
        user_id=user_sign_up(request.json)
        if(user_id):
            return jsonify({"message": "User saved successfully, User Id:" + str(user_id)}), 201
        else:
            return jsonify({"message": "Something went wrong!"}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": "Something went wrong"}), 500
    


# Method for signing up
@app.route('/signup', methods=['POST'])
@require_basic_auth
def sign_up_api():
    try:
        print(request.json)
        user_id=user_sign_up(request.json)
        if(user_id):
            return jsonify({"message": "User saved successfully, User Id:" + str(user_id)}), 201
        else:
            return jsonify({"message": "Something went wrong!"}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Method for logging in
@app.route('/login', methods=['POST'])
@require_basic_auth
def login_api():
    user_data = DAOs.UserData.from_json(request.json)
    return tcapi.login_api(user_data)


#uncomment for api testing
if __name__ == '__main__':
    app.run(debug=True)


#uncomment for local testing
'''
@require_basic_auth
def tenant_matching_api_local():
    # JSON data as a string
    user_preferences_json = {
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
    }

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
'''
