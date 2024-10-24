import mysql.connector
from mysql.connector import Error
import configparser

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get database configurations from config.ini
db_config = {
    'host': config['database']['host'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'database': config['database']['database']
}

# Function to create a connection to the MySQL database
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: '{e}' occurred while connecting to MySQL database")
    return connection

# Function to close the connection
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed")
