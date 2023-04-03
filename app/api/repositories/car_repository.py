from app.api.models.car import Car
from pymongo.database import Database

# CarRepository class
#
# This class is responsible for accessing the database to get the cars.
# It will be called by the service layer to get the data.
# It will also handle any exceptions that are raised by the database.

CAR_COLLECTION = "cars"


class CarRepository:
    def __init__(self, database: Database):
        self._database = database

    def get_all(self):
        # Access the database to get the cars.
        # Reminder: Transform the data that comes as a cursor into a list of Car objects.
        # Ex: list(db.find())
        pass

    def get_by_id(self, car_id: int):
        pass

    def create(self, car_data: Car):
        # On create we need to convert car_data to dict and then insert it into the database.
        # Ex: db.insert_one(car_data.dict())
        pass

    def update(self, car_id: int, car_data: Car):
        pass

    def delete(self, car_id: int):
        pass
