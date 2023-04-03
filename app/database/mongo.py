from pymongo import MongoClient
from pymongo.database import Database
from mongomock import MongoClient as MockMongoClient
from os import getenv

# The variable MONGODB_HOST is set dynamically.
#
# If the MONGODB_HOST environment variable is set, it will be used.
# Otherwise, the default value will be used.
#
# The idea is that inside the Docker container, the environment variable
# will exist and will be used, while outside the container, the default
# value will be used.
#
# Define the environment variable in Dockerfile / docker-compose.yml
MONGODB_HOST = getenv(
    "MONGODB_HOST", "mongodb://mongo_user:mongo_password@localhost:27017")

DATABASE_NAME = "veiculos-via-montadora"

# Connect to MongoDB.
_client = MongoClient(MONGODB_HOST)

# Access database.
_database = _client[DATABASE_NAME]


# This function returns the database.
# With the database object we can access collections.
# We can also create/delete new collections.
#
# If the MOCK_DATABASE environment variable is set to True,
# a mocked database will be returned instead of the real database.
def get_database() -> Database:
    is_test = getenv("MOCK_DATABASE", "false")
    if str.lower(is_test) == "true":
        return get_mock_database()
    return _database


# This function returns a mock database.
# It is used for testing.
def get_mock_database():
    _client = MockMongoClient()
    _database = _client[DATABASE_NAME]
    return _database
