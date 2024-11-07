from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import configparser
import os

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../config.ini'))

# Extract database configurations
db_config = {
    'host': config['database']['host'],
    'user': config['database']['user'],
    'password': config['database']['password'],
    'database': config['database']['database']
}

# Construct database URL
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
print(DATABASE_URL)
# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # Define the Base for models to inherit