from app.DataAccessObjects.DAOs import PropertyObject
from app.routes import TraceRentAPIInvoker as tcapi
from collections import defaultdict
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import List
from TraceRentBackend.TenantMatchingIMPL import generate_key

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
import configparser
from pathlib import Path

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
    if distance<=min_distance:
        return 5

    percentage_diff = ((distance - min_distance) / min_distance) * 100

    if percentage_diff <= 10:
        points = 5
    elif 10 < percentage_diff < 20:
        points = 4.5
    elif 20 <= percentage_diff < 25:
        points = 4
    elif 25 <= percentage_diff < 30:
        points = 3.5
    elif 30 <= percentage_diff < 35:
        points = 3
    elif 35 <= percentage_diff < 40:
        points = 2.5
    elif 40 <= percentage_diff < 45:
        points = 2
    else:
        points = 1.5 if percentage_diff <= 50 else 1

    return points


def assign_points_for_price(customer_price, rent):
    """
    Assign points based on the percentage difference between the customer price and the property price.
    The lower price will be used as the benchmark.

    :param customer_price: float - The price the customer is looking for.
    :param rent: float - The price of the property.
    :return: float - Points based on the comparison.
    """

    if customer_price<rent:
        return 5

    # Determine the minimum price as the benchmark
    min_price = min(customer_price, rent)

    # Calculate percentage difference
    percentage_diff = ((rent - min_price) / min_price) * 100

    # Assign points based on percentage difference
    if percentage_diff <= 10:
        points = 5
    elif 10 < percentage_diff < 20:
        points = 4.5
    elif 20 <= percentage_diff < 25:
        points = 4
    elif 25 <= percentage_diff < 30:
        points = 3.5
    elif 30 <= percentage_diff < 35:
        points = 3
    elif 35 <= percentage_diff < 40:
        points = 2.5
    elif 40 <= percentage_diff < 45:
        points = 2
    else:
        points = 1.5 if percentage_diff <= 50 else 1

    return points


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
    return int(min_price)


def getMinimumDistance(data:PropertyObject):
    min_dist = float('inf')
    for obj in data:
        if obj["distance"] is not None and obj["distance"] < min_dist and obj["distance"] != 0:  # Check if distance is set
            min_dist = obj["distance"]
    return int(min_dist) if min_dist != float('inf') else None  # Return None if no valid distance is found

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

        value["points"] = points
        print(value)

    sorted_points_list = sorted(data, key=lambda x: x["points"], reverse=True)

    return sorted_points_list


def getPriceRange(budget_category_id:int):
    minMax = tcapi.getLocationResponse(budget_category_id)
    return minMax



def get_price_ranges(t):
    print(t)
    start, end = t
    step = (end - start) // 3


    remainder = (end - start) % 3
    if remainder != 0:
        return [
                   (start, start + step + (1 if i == 0 else 0)) for i, start in
                   enumerate([start, start + step, start + 2 * step])
               ] + [(start + 2 * step + 1, end)]

    return [
        (start, start + step),
        (start + step, start + 2 * step),
        (start + 2 * step, end),
    ]


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
    percent_range_dict = defaultdict(list)

    # Iterate over the sorted list of properties and categorize based on percent_close
    for property_obj in sorted_property_list:
        percent_close = property_obj["percent_close"]

        # Determine the percent range
        if percent_close >= 90:
            range_key = "100-90"
        elif percent_close >= 80:
            range_key = "89-80"
        elif percent_close >= 70:
            range_key = "79-70"
        elif percent_close >= 60:
            range_key = "69-60"
        elif percent_close >= 50:
            range_key = "59-50"
        elif percent_close >= 40:
            range_key = "49-40"
        elif percent_close >= 30:
            range_key = "39-30"
        elif percent_close >= 20:
            range_key = "29-20"
        elif percent_close >= 10:
            range_key = "19-10"
        elif percent_close >= 0:
            range_key = "9-0"

        # Add the property to the appropriate range
        percent_range_dict[range_key].append(property_obj)

    # Convert defaultdict to regular dict
    return dict(percent_range_dict)



