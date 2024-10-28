import configparser


def load_properties(file_path):
    """
    Load properties from the given properties file.

    :param file_path: str - The path to the properties file.
    :return: dict - Dictionary containing the properties.
    """
    config = configparser.ConfigParser()

    # Read the file
    config.read(file_path)

    # Convert properties to dictionary format
    properties = {key: value for section in config.sections() for key, value in config.items(section)}

    return properties


def get_property(properties, key):
    """
    Retrieve a specific property value from the properties dictionary.

    :param properties: dict - Dictionary containing properties.
    :param key: str - The property key you want to fetch.
    :return: str - The value associated with the key.
    """
    return properties.get(key, None)