import requests
import ConfigConstants as config

# add comments
def getLocationResponse(location, params=None, headers=None):
    """
    Makes a GET request to the specified URL and returns the JSON response as an array.

    :param location: str - The endpoint location for the API.
    :param params: dict - (Optional) Query parameters to be sent with the request.
    :param headers: dict - (Optional) Headers to be sent with the request.
    :return: list - The JSON response from the API as a list of dictionaries.
    """

    properties = config.load_properties('TenantMatchingConfig.properties')
    url = config.get_property(properties, "TRACERENT_API_URL")

    try:
        # Make the GET request
        response = requests.get(url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the response as JSON
        json_data = response.json()

        # Ensure the response is a list (JSON array)
        if isinstance(json_data, list):
            return json_data
        else:
            # Return as a list with a single item if it's not an array
            return [json_data]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g., 404 Not Found
    except Exception as err:
        print(f"An error occurred: {err}")  # Other errors (e.g., connection errors)

    # Return an empty list if there was an error
    return []


def fetch_data_from_api(location, price, params=None, headers=None):
    """
    Makes a GET request to the specified URL and returns the JSON response.

    :param url: str - The endpoint URL of the API.
    :param params: dict - (Optional) Query parameters to be sent with the request.
    :param headers: dict - (Optional) Headers to be sent with the request.
    :return: dict - The JSON response from the API.
    """

    properties = config.load_properties('TenantMatchingConfig.properties')
    url = config.get_property(properties, "TRACERENT_API_URL")
    try:
        # Make the GET request
        response = requests.get(url, params=params, headers=headers)

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        # Parse the response as JSON
        json_data = response.json()
        return json_data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # e.g. 404 Not Found
    except Exception as err:
        print(f"An error occurred: {err}")  # Other errors (e.g., connection errors)
