import math
import TraceRentAPIInvoker as tcapi


def calculate_distance(ref_point, target_point):
    ref_x, ref_y = ref_point
    target_x, target_y = target_point

    distance = math.sqrt((target_x - ref_x) ** 2 + (target_y - ref_y) ** 2)

    return distance


def assign_points_for_distance(distance, min_distance):

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

def assign_points_for_price(customer_price, property_price):
    """
    Assign points based on the percentage difference between the customer price and the property price.
    The lower price will be used as the benchmark.

    :param customer_price: float - The price the customer is looking for.
    :param property_price: float - The price of the property.
    :return: float - Points based on the comparison.
    """

    # Determine the minimum price as the benchmark
    min_price = min(customer_price, property_price)

    # Calculate percentage difference
    percentage_diff = ((property_price - min_price) / min_price) * 100

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


def calculatePoints(distance, price, a, b, c, d, e, f, g, h, i):
    return distance + price + a + b + c + d + e + f + g + h + i


def getMinimumPropertyPrice(data):
    min_price = float('inf')
    for obj in data:
        if "price" in obj and obj["price"] < min_price:  # Check if "price" exists in the object
            min_price = obj["price"]

    return int(min_price)


def getMinimumDistance(data):
    min_dist = float('inf')
    for obj in data:
        if "distance" in obj and obj["distance"] < min_dist:  # Check if distance exists in the object
            min_dist = obj["distance"]

    return int(min_dist)


def calculateAndAddDistance(data, customer_coordinates):
    for value in data:
        value["distance"] = calculate_distance(value["coordinates"], customer_coordinates)

    return data


def assign_and_sort_property_list(data, customer_preferences,location):
    points_list = []
    customer_coordinates = None
    if location is not None:
        print("write code to get customer_coordinates as center of city") # write code to get customer_coordinates as center of city

    #comment coordinates later
    customer_coordinates = (32.333, -33.67)
    min_price = getMinimumPropertyPrice(data)

    data = calculateAndAddDistance(data, customer_coordinates)

    min_distance = getMinimumDistance(data)

    for value in data:
        property_price = value["price"]
        a = customer_preferences["a"]
        b = customer_preferences["b"]
        c = customer_preferences["c"]
        d = customer_preferences["d"]
        e = customer_preferences["e"]
        f = customer_preferences["f"]
        g = customer_preferences["g"]
        h = customer_preferences["h"]
        i = customer_preferences["i"]

        distance_points = assign_points_for_distance(value["distance"], min_distance)
        price_points = assign_points_for_price(min_price, property_price)

        points = calculatePoints(distance_points, price_points, a, b, c, d, e, f, g, h, i)

        value["points"] = points

    sorted_points_list = sorted(data, key=lambda x: x.get("points", 0), reverse=True)

    return sorted_points_list


def getPriceRange(location, x):
    list_props = tcapi.getLocationResponse(location)
    if list_props:
        # Step 1: Find the first and last valid prices in the sorted list
        a, b = None, None
        for item in list_props:
            price = item.get('price')
            if price is not None:  # Checking if the price is not None
                a = price
                break

        for item in reversed(list_props):
            price = item.get('price')
            if price is not None:  # Checking if the price is not None
                b = price
                break

        # Step 2: Create a list of three equal ranges between a and b if both are found
        if a is not None and b is not None:
            range_step = (b - a) / 3
            range_list = [
                (a, a + range_step),
                (a + range_step, a + 2 * range_step),
                (a + 2 * range_step, b)
            ]

            value1 = range_list[0][x]  # 300.0 from the first tuple
            value2 = range_list[1][x]  # 400.0 from the second tuple

            # Converting to integer if needed
            value1 = int(value1)
            value2 = int(value2)

            return (value1, value2)

        else:
            return None

    else :
        return None


def getMaxPoints(customer_preferences):
    a = int(customer_preferences["a"])
    b = int(customer_preferences["b"])
    c = int(customer_preferences["c"])
    d = int(customer_preferences["d"])
    e = int(customer_preferences["e"])
    f = int(customer_preferences["f"])
    g = int(customer_preferences["g"])
    h = int(customer_preferences["h"])
    i = int(customer_preferences["i"])

    return a+b+c+d+e+f+g+h+i+10


def percentage_close(a, b):
    if a == 0:  # To avoid division by zero
        return None

    # Calculate the percentage of how close b is to a
    percentage = (b / a) * 100

    return int(percentage)


def add_percent_close(sorted_property_list, reference_points):
    for property_obj in sorted_property_list:
        # Calculate percent close based on the reference price
        property_obj["percentClose"] = percentage_close(reference_points, property_obj["points"])

    return sorted_property_list