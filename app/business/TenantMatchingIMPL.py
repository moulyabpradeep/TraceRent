import math
from app.routes import TraceRentAPIInvoker as tcapi
from collections import defaultdict
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import List
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import configparser
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.DataAccessObjects.DAOs import PropertyObject

config = configparser.ConfigParser()
config_path = Path(__file__).resolve().parent.parent.parent / 'config.ini'  # Adjust this if necessary
config.read(config_path)

# Read the thresholds_points as a string and clean it
thresholds_points_str = config.get('tenant_matching_data', 'thresholds_points').strip()

# Function to parse the threshold points
def parse_thresholds(thresholds_str):
    return [
        (int(pair.split(',')[0].strip()), float(pair.split(',')[1].strip()))
        for pair in thresholds_str.split(';')
    ]


# Parse the thresholds points
thresholds_points = parse_thresholds(thresholds_points_str)
# Get fixed salt from config
salt = config.get('authentication', 'salt')

def generate_key(password: str) -> bytes:
    """
    Generate a symmetric encryption key from a password and fixed salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the key (AES-256)
        salt=salt.encode(),  # Convert the salt to bytes
        iterations=100000,  # Increase iterations for better security
        backend=default_backend()
    )
    return kdf.derive(password.encode())  # Derive the key from the password

def encrypt_password(password: str) -> str:
    """
    Encrypt a password using AES and encode the result with base32 to avoid special characters.
    """
    key = generate_key(password)  # Generate the symmetric key using the password
    iv = os.urandom(16)  # Generate a random IV (Initialization Vector) for AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())  # AES encryption setup
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(password.encode()) + encryptor.finalize()  # Encrypt the password

    # Concatenate IV and encrypted password, then encode as base32 to avoid special characters
    encrypted_password = base64.b32encode(iv + encrypted).decode('utf-8')  # Ensure it is decoded to string
    return encrypted_password

def decrypt_password(encrypted_password: str, password: str) -> bytes:
    """
    Decrypt an encrypted password using AES and base32 decoding.
    This method returns binary data instead of decoding into a string.
    """
    key = generate_key(password)  # Generate the symmetric key using the password
    encrypted_data = base64.b32decode(encrypted_password.encode('utf-8'))  # Decode from base32 to bytes

    # Check that the encrypted data is long enough to contain the IV and encrypted text
    if len(encrypted_data) < 16:
        raise ValueError("Invalid encrypted data (IV length mismatch).")

    iv, encrypted = encrypted_data[:16], encrypted_data[16:]  # Extract the IV (first 16 bytes) and the rest as encrypted data

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())  # AES decryption setup
    decryptor = cipher.decryptor()
    decrypted_password = decryptor.update(encrypted) + decryptor.finalize()  # Decrypt the password
    return decrypted_password  # Return the decrypted data as bytes


def get_city_coordinates(city_name):
    geolocator = Nominatim(user_agent="city_locator")
    location = geolocator.geocode(city_name)

    if location:
        return location.latitude, location.longitude
    else:
        return None


def calculate_distance(coord1, coord2):
    # coord1 and coord2 should be tuples of the form (latitude, longitude)
    distance = geodesic(coord1, coord2).kilometers  # You can use .miles for distance in miles
    return distance


def assign_points_for_distance(distance, min_distance):
    """
    Assigns points based on the distance compared to a minimum threshold.

    Parameters:
        distance (float): The actual distance to evaluate.
        min_distance (float): The minimum threshold distance for maximum points.

    Returns:
        float: Points awarded based on the distance percentage difference from the minimum.
    """
    print('PROP DIST'+str(distance))
    print('mindist' +str(min_distance))
    default_points = 1.0  # Points if distance exceeds 50% of min_distance

    if min_distance==0:
        min_distance=1

    # If distance is less than or equal to minimum, award max points
    if distance <= min_distance:
        return 5.0

    # Calculate the percentage difference
    percentage_difference = ((distance - min_distance) / min_distance) * 100

    # Find the appropriate points based on percentage difference
    for threshold, points in thresholds_points:
        if percentage_difference <= threshold:
            return points

    # Return default points if no threshold matches
    return default_points


def assign_points_for_price(customer_price, property_price):
    """
    Assigns points based on the percentage difference between the customer price and the property price,
    using the lower price as the benchmark.

    Parameters:
        customer_price (float): The price the customer is willing to pay.
        property_price (float): The price of the property.

    Returns:
        float: Points awarded based on the price comparison.
    """
    print('CUSTOMER PRICE'+str(customer_price))
    print('PROPERTY PRICE' + str(property_price))
    # Check if the customer price is less than or equal to the property price
    if property_price <= customer_price:
        return 5.0  # Max points for reasonable price range (this logic might change as needed)

    # Read the thresholds_points_price from the config and parse it
    thresholds_points_price_str = config.get('tenant_matching_data', 'thresholds_points_price').strip()
    thresholds_points_price = parse_thresholds(thresholds_points_price_str)

    default_points = 1.0  # Points if percentage difference exceeds all defined thresholds

    # Use the minimum price as the benchmark for calculating percentage difference
    min_price = min(customer_price, property_price)

    # Avoid division by zero if min_price is zero (although this should not happen in a valid context)
    if min_price == 0:
        return default_points

    # Calculate the percentage difference between the prices
    percentage_difference = ((property_price - min_price) / min_price) * 100

    # Debug: print percentage difference to understand the flow
    print(f"Percentage difference: {percentage_difference}%")

    # Assign points based on the percentage difference and thresholds
    for threshold, points in thresholds_points_price:
        if percentage_difference <= threshold:
            return points

    # Return default points if no threshold matches
    return default_points


def calculatePoints(customer_preferences, distance_points, price_points,
                    school_proximity_points, hospital_proximity_points, transit_proximity_points,
                    in_house_laundry, gym, pet_friendly, pool):
    points = distance_points + price_points + school_proximity_points + hospital_proximity_points + transit_proximity_points

    if customer_preferences.in_house_laundry is not None and customer_preferences.in_house_laundry is True and in_house_laundry is True:
        points += 1
    if customer_preferences.gym is not None and customer_preferences.gym is True and gym is True:
        points += 1
    if customer_preferences.pet_friendly is not None and customer_preferences.pet_friendly is True and pet_friendly is True:
        points += 1
    if customer_preferences.pool is not None and customer_preferences.pool is True and pool is True:
        points += 1

    return points


def getMinimumPropertyPrice(data: PropertyObject):
    min_price = float('inf')
    for obj in data:
        if obj["rent"] < min_price:
            min_price = obj["rent"]
    print("&&&&&&&&&&&&&&&&&&&&&&&&")
    print(str(float(min_price)))
    return float(min_price)


def getMinimumDistance(data:PropertyObject):
   min_dist = float('inf')
   for obj in data:
        if obj["distance"] is not None and obj["distance"] < min_dist and obj["distance"] != 0:  # Check if distance is set
            print("%%%%%%%%%%%%%%%%%%%%%%")
            print(str(obj["property_coordinates"]))
            min_dist = obj["distance"]
   return float(min_dist) if min_dist != float('inf') else None  # Return None if no valid distance is found


from decimal import Decimal


def calculateAndAddDistance(data, customer_coordinates):
    for obj in data:
        # Ensure latitude and longitude are present
        if "latitude" in obj and "longitude" in obj:
            property_coordinates = (
                float(obj["latitude"]),  # Convert from Decimal to float
                float(obj["longitude"])
            )
            obj["property_coordinates"] = property_coordinates
        else:
            print("Missing keys in object:", obj)
        print(obj["property_coordinates"])
        obj["distance"] = calculate_distance(property_coordinates, customer_coordinates)
        
    return data


def assign_and_sort_property_list(data:PropertyObject, customer_preferences, city, max_points)->List[PropertyObject]:
    points_list = []
    city_coordinates = None
    if city is not None:
        city_coordinates = get_city_coordinates(city)

        if city_coordinates:
            print(
                f"The coordinates of the middle of {city} are: Latitude = {city_coordinates[0]}, Longitude = {city_coordinates[1]}")
        else:
            print(f"Could not find coordinates for {city}.")

    # comment coordinates later
   # city_coordinates = (32.333, -33.67)
    min_price = getMinimumPropertyPrice(data)

    data = calculateAndAddDistance(data, city_coordinates)
    customer_school_proximity_weight = customer_preferences.school_proximity
    customer_transit_proximity_weight = customer_preferences.transit_proximity
    customer_hospital_proximity_weight = customer_preferences.hospital_proximity
    min_distance = getMinimumDistance(data)
    print(min_distance)
    for value in data:
        rent = value["rent"]
        school_proximity = value["school_proximity"]
        hospital_proximity = value["hospital_proximity"]
        transit_proximity = value["transit_proximity"]
        in_house_laundry = value["in_house_laundry"]
        gym = value["gym"]
        pet_friendly = value["pet_friendly"]
        pool = value["pool"]
        distance = value["distance"]
        print(str(min_distance))
        distance_points = assign_points_for_distance(distance, min_distance)
        price_points = assign_points_for_price(min_price, rent)
        school_proximity_points = proximity_points(customer_school_proximity_weight,school_proximity, 2000)
        hospital_proximity_points = proximity_points(customer_hospital_proximity_weight,hospital_proximity, 10000)
        transit_proximity_points = proximity_points(customer_transit_proximity_weight,transit_proximity, 1000)

        points = calculatePoints(customer_preferences, distance_points, price_points,
                                 school_proximity_points, hospital_proximity_points, transit_proximity_points,
                                 in_house_laundry, gym, pet_friendly, pool)

        value["school_proximity_points"] = school_proximity_points
        value["hospital_proximity_points"] = hospital_proximity_points
        value["transit_proximity_points"] = transit_proximity_points
        value["max_points"] = max_points
        value["price_points"] = price_points
        value["distance_points"] = distance_points

        value["points"] = points
        print(value)

    sorted_points_list = sorted(data, key=lambda x: x["points"], reverse=True)

    return sorted_points_list


def getPriceRange(budget_category_id:int):
    minMax = tcapi.getLocationResponse(budget_category_id)
    return minMax


def divide_range(input_tuple):
    a, b = input_tuple
    range_step = 300
    ranges = []

    for start in range(a, b + 1, range_step):
        end = min(start + range_step, b + 1)  # Ensure the end does not exceed b
        ranges.append((start, end))

    return ranges


def getMaxPoints(customer_preferences):
    points = 10+customer_preferences.school_proximity + customer_preferences.school_proximity + customer_preferences.school_proximity

    if customer_preferences.in_house_laundry is not None and customer_preferences.in_house_laundry is True:
        points += 1
    if customer_preferences.gym is not None and customer_preferences.gym is True:
        points += 1
    if customer_preferences.pet_friendly is not None and customer_preferences.pet_friendly is True:
        points += 1
    if customer_preferences.pool is not None and customer_preferences.pool is True:
        points += 1
    return points


def percentage_close(a, b):
    if a == 0:  # To avoid division by zero
        return None

    # Calculate the percentage of how close b is to a
    percentage = (b / a) * 100

    return int(percentage)


def add_percent_close(sorted_property_list, reference_points):
    for property_obj in sorted_property_list:
        # Calculate percent close based on the reference price
        property_obj["percent_close"] = percentage_close(reference_points, property_obj["points"])

    return sorted_property_list


def proximity_points(weight, proximity, benchmark):
    if proximity < benchmark:
        return weight

    # Calculate percentage difference
    percentage_diff = ((proximity - benchmark) / benchmark) * 100

    # Assign points based on percentage difference
    if percentage_diff <= 20:
        return weight
    elif 20 < percentage_diff < 40:
        points = weight - 0.5
    elif 40 <= percentage_diff < 60:
        points = weight - 1
    elif 60 <= percentage_diff < 80:
        points = weight - 1.5
    else:
        points = points = weight - 2.5

    if points < 0:
        return 0

    return points


def categorize_properties_by_percent_close(sorted_property_list):
    """
    Categorizes properties into ranges based on their percent_close attribute.

    Parameters:
        sorted_property_list (list): A list of property objects, each with a percent_close attribute.

    Returns:
        dict: A dictionary where keys are range labels, and values are lists of properties within each range.
    """

    # Define percent ranges and their corresponding labels
    percent_ranges_str = config.get('tenant_matching_data', 'percent_ranges')
    percent_ranges = [
        (int(r.split('-')[0]), int(r.split('-')[1]), f"{r.split('-')[0]}-{r.split('-')[1]}")
        for r in percent_ranges_str.split(', ')
    ]

    # Initialize a dictionary to store properties categorized by ranges
    percent_range_dict = defaultdict(list)

    # Iterate over the properties and categorize each by percent_close
    for property_obj in sorted_property_list:
        percent_close = property_obj['percent_close']

        # Find the appropriate range for the percent_close value
        for min_range, max_range, label in percent_ranges:
            if min_range <= percent_close <= max_range:
                percent_range_dict[label].append(property_obj)
                break  # Stop once the correct range is found

    # Return the dictionary containing categorized properties
    return dict(percent_range_dict)


def get_price_ranges(t):
    start, end = t
    step = (end - start) // 3
    remainder = (end - start) % 3

    if remainder != 0:
        # Distribute the remainder across the first ranges
        return [
            (start, start + step + (1 if remainder > 0 else 0)),  # First range gets an extra 1 if remainder exists
            (start + step + (1 if remainder > 0 else 0), start + 2 * step + (1 if remainder > 1 else 0)),  # Second range gets an extra 1 if remainder > 1
            (start + 2 * step + (1 if remainder > 1 else 0), end)  # Last range takes the rest
        ]

    return [
        (start, start + step),
        (start + step, start + 2 * step),
        (start + 2 * step, end),
    ]



def send_email_to_owner(recipient_email):
    # SMTP server configuration
    smtp_server = config.get('email', 'smtp_server')
    smtp_port = config.getint('email', 'smtp_port')
    sender_email = config.get('email', 'sender_email')
    sender_password = config.get('email', 'password')

    # Email message content
    subject = config.get('email', 'subject')
    body = config.get('email', 'body')

    # Debug output
    print("Sending email from:", sender_email)

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server with SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Enable debug output
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Email sent successfully!")
            return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False



