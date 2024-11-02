import requests
import configparser


def getLocationResponse(location, params=None, headers=None):
    """
    Makes a GET request to the specified URL and returns the JSON response as an array.

    :param location: str - The endpoint location for the API.
    :param params: dict - (Optional) Query parameters to be sent with the request.
    :param headers: dict - (Optional) Headers to be sent with the request.
    :return: list - The JSON response from the API as a list of dictionaries.
    """

    # Initialize configparser and read the configuration file
    config = configparser.ConfigParser()
    config.read(r'D:\Downloads\TraceRent_AI-Tracerent-Backend\TraceRent_AI-Tracerent-Backend\config.ini')

    # Access the TRACERENT_API_URL under a specific section
    # Replace 'Settings' with the actual section name in your config.ini
    url = config.get('api details', 'TRACERENT_API_URL')

    try:
        # Make the GET request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parse the response as JSON
        json_data = response.json()

        # Ensure the response is a list (JSON array)
        return json_data if isinstance(json_data, list) else [json_data]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return []


def fetch_data_from_api(location, price, params=None, headers=None):
    """
    Makes a GET request to the specified URL and returns the JSON response.

    :param location: str - The endpoint location for the API.
    :param params: dict - (Optional) Query parameters to be sent with the request.
    :param headers: dict - (Optional) Headers to be sent with the request.
    :return: dict - The JSON response from the API.
    """

    config = configparser.ConfigParser()
    config.read(r'D:\Downloads\TraceRent_AI-Tracerent-Backend\TraceRent_AI-Tracerent-Backend\config.ini')

    # Access the TRACERENT_API_URL under a specific section
    url = config.get('api details', 'TRACERENT_API_URL')

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return {}
