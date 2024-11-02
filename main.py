from flask import Flask, request, jsonify
import configparser
from app.business import TenantMatchingIMPL as impl
from app.routes import TraceRentAPIInvoker as api

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
    priceTag = customer_preferences["price"]
    location = customer_preferences["location"]

    # Load properties
    properties_file_path = r"D:\Downloads\TraceRent_AI-Tracerent-Backend\TraceRent_AI-Tracerent-Backend\config.ini"
    properties = load_properties(properties_file_path)

    # Accessing properties using the section names
    priceRange = impl.getPriceRange(location, priceTag)
    data = api.fetch_data_from_api(location, priceRange, params=None, headers=None)

    # Sample data (for testing)
    data = [
        {
            "price": 1500,
            "location": "Calgary",
            "coordinates": (22, 91),
            "a": 1,
            "b": 3,
            "c": 5,
            "d": 1,
            "e": 3,
            "f": 5,
            "g": 1,
            "h": 3,
            "i": 5
        },
        {
            "price": 1000,
            "location": "Calgary",
            "coordinates": (-22, 51),
            "a": 1,
            "b": 3,
            "c": 5,
            "d": 1,
            "e": 3,
            "f": 5,
            "g": 1,
            "h": 3,
            "i": 5
        }
    ]

    if not data:
        return None

    maxPoints = impl.getMaxPoints(customer_preferences)
    sorted_property_list = impl.assign_and_sort_property_list(data, customer_preferences, location)
    final_list = impl.add_percent_close(sorted_property_list, maxPoints)

    return final_list


# Define the route to access tenantMatching method
@app.route('/tenantMatching', methods=['POST'])
def tenant_matching_api():
    customer_preferences = request.json
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
    preferences = request.json
    # TODO: Implement the logic to save preferences
    return jsonify({"message": "Save preferences logic not implemented"}), 200


if __name__ == '__main__':
    app.run(debug=True)
