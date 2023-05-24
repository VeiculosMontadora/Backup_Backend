from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Api configs.
    API_TITLE = "VEICULOS_VIA_MONTADORA"
    API_HOST = "0.0.0.0"
    API_PORT = 8000

    # DB configs.
    #
    # The variable DB_HOST is set dynamically.
    # If the MONGODB_HOST environment variable is set, it will be used.
    # Otherwise, the default value will be used.
    #
    # If using Docker, define the environment variable in Dockerfile / docker-compose.yml
    DB_HOST = getenv(
        "MONGODB_HOST", "mongodb://mongo_user:mongo_password@localhost:27017")
    DB_NAME = "veiculos-via-montadora"
    #
    # DB ENV for runing tests.
    # Set the 'DB_ENVIRONMENT' environment variable to 'test' when running tests.
    DB_ENVIRONMENT = "prod"


settings = Settings()
