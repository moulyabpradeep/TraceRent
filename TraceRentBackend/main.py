import configparser
import TenantMatchingIMPL as impl
import TraceRentAPIInvoker as api


# Load properties from the file
def load_properties(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def tenantMatching(customer_preferences):
    print('testing')
    rangeFound = False
    final_list = None
    priceTag = customer_preferences["price"]
    location = customer_preferences["location"]

    # Load properties
    properties_file_path = r"C:\Users\udogr\PycharmProjects\TraceRent Tenant Matching\TenantMatchingConfig.properties"
    properties = load_properties(properties_file_path)

    # Accessing properties using the section names
    priceRange = impl.getPriceRange(location, priceTag)

    data = api.fetch_data_from_api(location, priceRange, params=None, headers=None)

    #comment data below later
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

    if data:

        maxPoints = impl.getMaxPoints(customer_preferences)
        sorted_property_list = impl.assign_and_sort_property_list(data, customer_preferences,location)

        final_list = impl.add_percent_close(sorted_property_list, maxPoints)

    return final_list


# Define customer preferences dictionary
customer_preferenceTest = {
    "price": 1,
    "location": "Calgary",
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

# Now call the tenantMatching function
testing = tenantMatching(customer_preferenceTest)
print(testing)  # Print the result to verify
