import requests
import mysql.connector
from mysql.connector import Error
import configparser
from pathlib import Path
from flask import Flask, request, jsonify


def getLocationResponse(location, params=None, headers=None):
    """
    Fetches location data from the SQL database based on the provided location.

    :param location: str - The location to filter the database records.
    :param params: dict - (Optional) Additional parameters for the SQL query.
    :return: list - The records retrieved from the database.
    """
    #Comment after local testing
    return None
    # Initialize configparser and read the configuration file
    config = configparser.ConfigParser()
    print("Initialized ConfigParser.")

    # Construct the path to the config.ini file relative to the current file
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'  # Adjust this if necessary
    print(f"Config path resolved: {config_path}")

    config.read(config_path)
    print("Configuration file read.")

    # Access database connection details
    db_config = {
        'host': config.get('database', 'host'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }
    print(f"Database configuration retrieved: {db_config}")

    connection = None
    cursor = None
    try:
        # Connect to the database
        print("About to connect")
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        # Create a cursor object
        cursor = connection.cursor(dictionary=True)
        print("Cursor created.")

        # Construct the SQL query
        query = "SELECT * FROM locations WHERE name = %s"  # Adjust the table name and condition as needed
        print(f"SQL query constructed: {query}")

        # Execute the query with parameters
        cursor.execute(query, (location,))
        print(f"Executed query with location: {location}")

        # Fetch all records
        records = cursor.fetchall()
        print(f"Fetched records: {records}")

        return records

    except mysql.connector.Error as err:
        print(f"Database error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
            print("Cursor closed.")
        if connection:
            connection.close()
            print("Database connection closed.")

    return []


def fetch_data_from_api(location, price, params=None, headers=None):
    """
    Fetches property data from the MySQL database based on location and price.

    :param location: str - The location for the property.
    :param price: str - The price information to filter properties.
    :param params: dict - (Optional) Additional query parameters to filter properties.
    :return: list - A list of property records from the database.
    """

    # Load database configuration
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'
    config.read(config_path)

    # Access the database connection details under a specific section
    db_config = {
        'host': config.get('database details', 'HOST'),
        'user': config.get('database details', 'USER'),
        'password': config.get('database details', 'PASSWORD'),
        'database': config.get('database details', 'DATABASE')
    }

    print(f"Database configuration retrieved: {db_config}")

    # Initialize a list to hold the results
    properties = []

    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Construct the query
        query = "SELECT * FROM properties WHERE location = %s AND price <= %s"
        parameters = (location, price)

        # Add additional filtering if params are provided
        if params:
            for key, value in params.items():
                query += f" AND {key} = %s"
                parameters += (value,)

        # Execute the query
        cursor.execute(query, parameters)
        properties = cursor.fetchall()

    except Error as db_err:
        print(f"Database error occurred: {db_err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    return properties


def save_preferences_to_db(preferences):
    #Comment after local testing
    #return jsonify({"message": "Preferences saved successfully!"}), 201
    # Initialize configparser and read the configuration file
    config = configparser.ConfigParser()
    print("Initialized ConfigParser.")

    # Construct the path to the config.ini file relative to the current file
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'
    print(f"Config path resolved: {config_path}")

    config.read(config_path)
    print("Configuration file read.")

    # Access database connection details
    db_config = {
        'host': config.get('database', 'host'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }
    print(f"Database configuration retrieved: {db_config}")

    # Helper function to retrieve value if key exists and is not None
    def get_pref_value(key):
        return preferences[key] if key in preferences and preferences[key] is not None else None

    # Define fields with checks for both existence and non-null values
    fields = {
        'user_id': get_pref_value('userId'),
        'tenant_category_id': get_pref_value('tenantCategoryId'),
        'location_category_id': get_pref_value('locationCategoryId'),
        'budget_category_id': get_pref_value('budgetCategoryId'),
        'school_proximity': get_pref_value('schoolProximity'),
        'hospital_proximity': get_pref_value('hospitalProximity'),
        'transit_proximity': get_pref_value('transitProximity'),
        'laundry': get_pref_value('laundry'),
        'gym': get_pref_value('gym'),
        'pet_friendly': get_pref_value('petFriendly'),
        'pool': get_pref_value('pool')
    }

    # Filter out keys that have None values
    filtered_fields = {key: value for key, value in fields.items() if value is not None}

    if not filtered_fields:
        return jsonify({"error": "No valid preferences to save."}), 400

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        cursor = connection.cursor()

        # Build the dynamic INSERT query based on available fields
        columns = ', '.join(filtered_fields.keys())
        placeholders = ', '.join(['%s'] * len(filtered_fields))
        insert_query = f"INSERT INTO user_preferences ({columns}) VALUES ({placeholders})"

        # Execute the query with filtered values
        cursor.execute(insert_query, tuple(filtered_fields.values()))
        connection.commit()
        print("Preferences successfully saved to the database.")

        return jsonify({"message": "Preferences saved successfully!"}), 201

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return jsonify({"error": "Database connection error"}), 500

    finally:
        # Ensure the connection is closed
        if 'cursor' in locals() and cursor:
            cursor.close()
            print("Database cursor closed.")
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")


def search_properties(preferences, price):
    # comment later after local testing
    return None
    # Initialize configparser and read the configuration file
    config = configparser.ConfigParser()
    print("Initialized ConfigParser.")

    # Construct the path to the config.ini file relative to the current file
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'  # Adjust path as necessary
    print(f"Config path resolved: {config_path}")

    config.read(config_path)
    print("Configuration file read.")

    # Access database connection details
    db_config = {
        'host': config.get('database', 'host'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }
    print(f"Database configuration retrieved: {db_config}")

    # Helper function to retrieve value if key exists and is not None
    def get_pref_value(key):
        return preferences[key] if key in preferences and preferences[key] is not None else None

    # Define search criteria with explicit checks
    search_criteria = {
        'tenant_category_id': get_pref_value('tenantCategoryId'),
        'location_category_id': get_pref_value('locationCategoryId'),
        'budget_category_id': get_pref_value('budgetCategoryId')
    }

    # Boolean fields only included if they are true
    boolean_fields = {
        'laundry': get_pref_value('laundry'),
        'gym': get_pref_value('gym'),
        'pet_friendly': get_pref_value('petFriendly'),
        'pool': get_pref_value('pool')
    }

    # Price range
    price_range = get_pref_value('priceRange')  # Expected to be a tuple (min_price, max_price)

    # Build query conditions for search criteria
    conditions = []
    values = []

    # Add numeric and category-based search criteria
    for key, value in search_criteria.items():
        if value is not None:
            conditions.append(f"{key} = %s")
            values.append(value)

    # Add Boolean fields to the search query only if they are True
    for key, value in boolean_fields.items():
        if value is True:  # Only include if explicitly True
            conditions.append(f"{key} = %s")
            values.append(1)  # Represent True as 1 for MySQL

    # Add price range to the search query if specified
    if price_range and isinstance(price_range, tuple) and len(price_range) == 2:
        min_price, max_price = price_range
        if min_price is not None and max_price is not None:
            conditions.append("price BETWEEN %s AND %s")
            values.extend([min_price, max_price])
        elif min_price is not None:
            conditions.append("price >= %s")
            values.append(min_price)
        elif max_price is not None:
            conditions.append("price <= %s")
            values.append(max_price)

    # Construct the query
    query = "SELECT * FROM properties"  # Assuming table name is 'properties'
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    print(f"Constructed query: {query}")

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as a list of dictionaries
        cursor.execute(query, values)

        # Fetch all results
        properties = cursor.fetchall()
        print("Properties successfully fetched from the database.")

        # Return as a list of dictionaries
        return properties if properties else []

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return []

    finally:
        # Ensure the connection is closed
        if 'cursor' in locals() and cursor:
            cursor.close()
            print("Database cursor closed.")
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")


def sign_up_api(preferences):
    #comment after local testing
    #return jsonify({"message": "Signup successful!"}), 201
    # Initialize ConfigParser and read the configuration file
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'  # Adjust path as necessary
    config.read(config_path)

    # Access database connection details
    db_config = {
        'host': config.get('database', 'host'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }

    # Required fields
    required_fields = ['name_of_user', 'user_email', 'user_phone', 'user_password', 'sessionId']

    # Check for missing fields
    for field in required_fields:
        if field not in preferences or preferences[field] is None:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Assign fields after validation
    name_of_user = preferences['name_of_user']
    user_email = preferences['user_email']
    user_phone = preferences['user_phone']
    user_password = preferences['user_password']
    session_id = preferences['sessionId']

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        cursor = connection.cursor(dictionary=True)

        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({"error": "Email already exists"}), 409

        # Insert new user into the database
        insert_query = """
        INSERT INTO users (name_of_user, user_email, user_phone, user_password, session_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name_of_user, user_email, user_phone, user_password, session_id))
        connection.commit()
        print("User successfully signed up.")

        return jsonify({"message": "Signup successful!"}), 201

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return jsonify({"error": "Database connection error"}), 500

    finally:
        # Ensure the connection is closed
        if 'cursor' in locals() and cursor:
            cursor.close()
            print("Database cursor closed.")
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")


def login_api(preferences):
    #Comment after local testing
    #return jsonify({"message": "Login successful!"}), 200
    # Initialize ConfigParser and read the configuration file
    config = configparser.ConfigParser()
    config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'  # Adjust path as necessary
    config.read(config_path)

    # Access database connection details
    db_config = {
        'host': config.get('database', 'host'),
        'port': config.get('database', 'port'),  # Database port (default is 3306)
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'database': config.get('database', 'database')
    }

    # Required fields for login
    required_fields = ['user_email', 'user_password']

    # Check for missing fields
    for field in required_fields:
        if field not in preferences or preferences[field] is None:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Retrieve email and password from preferences
    user_email = preferences['user_email']
    user_password = preferences['user_password']

    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        cursor = connection.cursor(dictionary=True)

        # Check if the email exists
        cursor.execute("SELECT user_password FROM users WHERE user_email = %s", (user_email,))
        user_record = cursor.fetchone()

        if user_record:
            # Compare provided password with stored password
            if user_password == user_record['user_password']:
                print("User successfully logged in.")
                return jsonify({"message": "Login successful!"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Email does not exist"}), 404

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return jsonify({"error": "Database connection error"}), 500

    finally:
        # Ensure the connection is closed
        if 'cursor' in locals() and cursor:
            cursor.close()
            print("Database cursor closed.")
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")