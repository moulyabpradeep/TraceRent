from flask import Flask, request, jsonify
from functools import wraps
import configparser
from app.DataAccessObjects.DAOs import PropertyObject
from app.business import TenantMatchingIMPL as impl
import os
from pathlib import Path
from app.DataAccessObjects import DAOs
import base64
from app.services.tenant_service import *
from app.services.property_service import *
from app.services.user_service import *
from http import HTTPStatus
import logging
from app import global_constants as const
from enum import Enum


app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Filter(Enum):
    LIKED = "LIKED"
    DISLIKED = "DISLIKED"
    VIEWED = "VIEWED"
    CONTACTED = "CONTACTED"


# Utility functions
def create_login_response(success: bool, message: str, status_code: int, user_info=None):
    """Standardized response format for JSON API responses, including user info."""
    return {
        "success": success,
        "message": message,
        "user_info": user_info if user_info else None
    }, status_code


def create_preferences_response(success: bool, message: str, status_code: int):
    """Standardized response format for JSON API responses."""
    return {
        "success": success,
        "message": message
    }, status_code


def create_signup_response(success: bool, message: str, status_code: int, additional_info=None):
    """Standardized response format for JSON API responses, with optional additional information."""
    response = {
        "success": success,
        "message": message
    }
    if additional_info is not None:
        response.update(additional_info)
    return response, status_code


def create_rating_standard_response(success: bool, message: str, status_code: int, additional_info=None):
    """Standardized response format for JSON API responses, with optional additional information."""
    response = {
        "success": success,
        "message": message
    }
    if additional_info is not None:
        response.update(additional_info)
    return response, status_code


def create_standard_response(success: bool, message: str, status_code: int, additional_info=None):
    """Standardized response format for JSON API responses, with optional additional information."""
    response = {
        "success": success,
        "message": message
    }
    if additional_info is not None:
        response.update(additional_info)
    return response, status_code


def check_auth(username, password):
    """Verify if the provided username and password are correct."""
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent / 'config.ini'

    config.read(config_path)
    auth_user = config.get('authentication', 'user')
    auth_password = config.get('authentication', 'password')

    return username == auth_user and password == auth_password


def create_range_standard_response(success: bool, message: str, status_code: int, additional_info: dict = None):
    """Standardized response format for JSON API responses."""
    response = {"success": success, "message": message}
    if additional_info:
        response.update(additional_info)
    return response, status_code


#Auth functions
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


#API ROUTES
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
    try:

        #TODO: Replace (0,1000) with method, return min and max as tuple
        price_range = 0,1000

        if price_range:
            logger.info("Price range fetched successfully.")
            list = impl.get_price_ranges(price_range)
            return create_range_standard_response(
                success=True,
                message=const.PRICE_RANGE_FETCH_SUCCESS_MSG,
                status_code=HTTPStatus.OK,
                additional_info={"price_range": list}
            )
        else:
            logger.warning("Price range not found.")
            return create_rating_standard_response(
                success=False,
                message=const.PRICE_RANGE_FETCH_FAILURE_MSG,
                status_code=HTTPStatus.OK
            )

    except Exception as e:
        logger.exception("Exception occurred while fetching price range.")
        return create_rating_standard_response(
            success=False,
            message=const.GENERAL_ERROR_MSG,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


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
        # Log the incoming request JSON
        logger.info("Received request for saving preferences: %s", request.json)

        # Attempt to save preferences
        if save_preferences_service(request.json):
            logger.info("Preferences successfully saved to the database.")
            return create_preferences_response(success=True, message=const.PREFERENCES_SAVE_SUCCESS,
                                            status_code=HTTPStatus.CREATED)
        else:
            logger.error("Failed to save preferences to the database.")
            return create_preferences_response(success=False, message=const.PREFERENCES_SAVE_FAILURE,
                                            status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.exception("Exception occurred while saving preferences: %s", e)
        return create_preferences_response(success=False, message=const.GENERAL_ERROR_MSG,
                                        status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


# Method for signing up
@app.route('/signup', methods=['POST'])
@require_basic_auth
def sign_up_api():
    try:
        # Log the incoming request JSON
        logger.info("Received sign-up request: %s", request.json)

        # Validate input
        data = request.get_json()
        if not data or "user_email" not in data:
            logger.warning("Invalid input for email.")
            return create_signup_response(success=False, message=const.INVALID_EMAIL_MSG, status_code=HTTPStatus.BAD_REQUEST)

        email = data.get("user_email")

        # Check if user already exists
        user = get_user_by_username(email)
        if user:
            logger.info("User already exists: %s", user)
            return create_signup_response(success=False, message=const.USER_EXISTS_MSG, status_code=HTTPStatus.CONFLICT, additional_info={"user": str(user)})

        # Attempt user registration
        user_id = user_sign_up(data)
        if user_id:
            logger.info("User saved successfully with User ID: %s", user_id)
            return create_signup_response(success=True, message=const.USER_SIGNUP_SUCCESS_MSG, status_code=HTTPStatus.CREATED, additional_info={"user_id": user_id})
        else:
            logger.error("Failed to save user.")
            return create_signup_response(success=False, message=const.GENERAL_ERROR_MSG, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.exception("Exception occurred during sign-up: %s", e)
        return create_signup_response(success=False, message=const.GENERAL_ERROR_MSG, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


# Method for logging in
@app.route('/login', methods=['GET'])
@require_basic_auth
def login_api():
    try:
        data = request.get_json()
        if not data or "user_password" not in data:
            return create_login_response(success=False, message=const.INVALID_PASSWORD_MSG, status_code=HTTPStatus.BAD_REQUEST)

        decoded_password = data.get("user_password")
        if not decoded_password:
            return create_login_response(success=False, message=const.INVALID_PASSWORD_MSG, status_code=HTTPStatus.BAD_REQUEST)

        # Retrieve user details from the database
        user_email = data.get("user_email")
        user = get_user_by_username(user_email)

        if not user:
            return create_login_response(success=False, message=const.USER_NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)

        user_password_from_db = user.get("password")
        decoded_password_from_db = impl.decrypt_password(user_password_from_db, decoded_password)

        # Validate password
        if user_password_from_db and decoded_password_from_db == decoded_password:
            return create_login_response(success=True, message=const.USER_FOUND_MSG, status_code=HTTPStatus.OK, user_info=user)
        else:
            return create_login_response(success=False, message=const.PASSWORD_INCORRECT_MSG, status_code=HTTPStatus.UNAUTHORIZED, user_info=None)

    except Exception as e:
        app.logger.error(f"Exception in login_api: {e}")
        return create_login_response(success=False, message=const.GENERAL_ERROR_MSG, status_code=HTTPStatus.INTERNAL_SERVER_ERROR, user_info=None)


# Empty method for rating properties
@app.route('/likeDislikeProperty', methods=['PUT'])
@require_basic_auth
def like_dislike_property():
    try:
        data = request.json
        if data is None:
            logger.warning("No data received for property rating.")
            return create_rating_standard_response(success=False, message=const.NO_DATA_MSG, status_code=HTTPStatus.BAD_REQUEST)

        # TODO: Replace `None` with actual database method call to fetch liked properties based on data, returns Boolean
        rated = handle_tenant_actions(data)

        # Check if properties were fetched successfully
        if rated is not None and rated == True:
            logger.info("Properties fetched successfully for rating.")
            return create_rating_standard_response(success=True, message=const.PROPERTIES_FETCH_SUCCESS_MSG, status_code=HTTPStatus.OK, additional_info={"rated": rated})
        else:
            logger.info("Unable to fetch properties")
            return create_rating_standard_response(success=False, message=const.PROPERTIES_FETCH_FAILURE_MSG, status_code=HTTPStatus.OK)

    except Exception as e:
        logger.exception("Exception occurred during property rating.")
        return create_rating_standard_response(success=False, message=const.GENERAL_ERROR_MSG, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


# Empty method for getting liked properties
@app.route('/likedProperties', methods=['GET'])
@require_basic_auth
def get_liked_properties():
    try:
        data = request.json
        print(data)
        if data is None:
            logger.warning("No data received for property rating.")
            return create_rating_standard_response(success=False, message=const.NO_DATA_MSG,
                                                   status_code=HTTPStatus.BAD_REQUEST)
        # TODO: Replace `[]` with actual database method call to fetch liked properties as a JSON array
        filter = const.LIKED_FILTER
        liked_properties = []
        liked_properties = get_properties_by_action(data.get("user_id"), filter)

        if liked_properties:
            logger.info("Liked properties fetched successfully.")
            return create_standard_response(
                success=True,
                message=const.PROPERTIES_FETCH_SUCCESS_MSG,
                status_code=HTTPStatus.OK,
                additional_info={"liked_properties": liked_properties}
            )
        else:
            logger.info("No properties found.")
            return create_standard_response(
                success=False,
                message=const.PROPERTIES_FETCH_FAILURE_MSG,
                status_code=HTTPStatus.OK
            )

    except Exception as e:
        logger.exception("Exception occurred while fetching liked properties.")
        return create_standard_response(
            success=False,
            message=const.GENERAL_ERROR_MSG,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


# Empty method for getting disliked properties
@app.route('/dislikedProperties', methods=['GET'])
@require_basic_auth
def get_disliked_properties():
    try:
        data = request.json
        if data is None:
            logger.warning("No data received for property rating.")
            return create_rating_standard_response(success=False, message=const.NO_DATA_MSG,
                                                   status_code=HTTPStatus.BAD_REQUEST)
        # TODO: Replace `[]` with actual database method call to fetch diliked properties as a JSON array
        filter = const.DISLIKED_FILTER
        disliked_properties = []
        disliked_properties = get_properties_by_action(data.get("user_id"), filter)

        if disliked_properties:
            logger.info("Disliked properties fetched successfully.")
            return create_standard_response(
                success=True,
                message=const.PROPERTIES_FETCH_SUCCESS_MSG,
                status_code=HTTPStatus.OK,
                additional_info={"disliked_properties": disliked_properties}
            )
        else:
            logger.info("No properties found.")
            return create_standard_response(
                success=False,
                message=const.PROPERTIES_FETCH_FAILURE_MSG,
                status_code=HTTPStatus.OK
            )

    except Exception as e:
        logger.exception("Exception occurred while fetching disliked properties.")
        return create_standard_response(
            success=False,
            message=const.GENERAL_ERROR_MSG,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


@app.route('/contactedProperties', methods=['GET'])
@require_basic_auth
def get_contacted_properties():
    try:
        data = request.json
        if data is None:
            logger.warning("No data received for contacted properties method.")
            return create_rating_standard_response(success=False, message=const.NO_DATA_MSG,
                                                   status_code=HTTPStatus.BAD_REQUEST)
        # TODO: Replace `[]` with actual database method call to fetch contacted properties as a JSON array
        contacted_properties = []
        filter = const.CONTACTED_FILTER
        contacted_properties = get_properties_by_action(data.get("user_id"), filter)

        if contacted_properties:
            logger.info("Contacted properties fetched successfully.")
            return create_standard_response(
                success=True,
                message=const.PROPERTIES_FETCH_SUCCESS_MSG,
                status_code=HTTPStatus.OK,
                additional_info={"contacted_properties": contacted_properties}
            )
        else:
            logger.info("No properties found.")
            return create_standard_response(
                success=False,
                message=const.PROPERTIES_FETCH_FAILURE_MSG,
                status_code=HTTPStatus.OK
            )

    except Exception as e:
        logger.exception("Exception occurred while fetching contacted properties.")
        return create_standard_response(
            success=False,
            message=const.GENERAL_ERROR_MSG,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR
        )


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


def login_api_local(data):
    try:
        # Parse request JSON
        if not data or "user_password" not in data:
            return create_location_response(success=False, message=INVALID_PASSWORD_MSG, status_code=HTTPStatus.BAD_REQUEST, user_info=None)

        decoded_password = data.get("user_password")
        if not decoded_password:
            return create_location_response(success=False, message=INVALID_PASSWORD_MSG, status_code=HTTPStatus.BAD_REQUEST, user_info=None)

        # Retrieve user details from the database
        user_email = data.get("user_email")
        user={
              "username": "john.doe@example.com",
              "password": "PUBX7KD7TLGLP7JYGHWWMGHT4TUKGP73LINO6TWAELBIEZ26WRPHY===",
             }

        if not user:
            return create_login_response(success=False, message=USER_NOT_FOUND_MSG, status_code=HTTPStatus.NOT_FOUND)

        user_password_from_db = user.get("password")
        decoded_password_from_db = impl.decrypt_password(user_password_from_db, decoded_password)

        # Validate password
        if user_password_from_db and decoded_password_from_db == decoded_password:
            return create_login_response(success=True, message=f"{USER_FOUND_MSG}, User: {str(user)}", status_code=HTTPStatus.OK)
        else:
            return create_login_response(success=False, message=PASSWORD_INCORRECT_MSG, status_code=HTTPStatus.UNAUTHORIZED)

    except Exception as e:
        app.logger.error(f"Exception in login_api: {e}")
        return create_login_response(success=False, message=GENERAL_ERROR_MSG, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


login_request = {
    "user_email": "john.doe@example.com",
    "user_password": "SecurePassword123",
}

login_api_local(login_request)
'''