# from fastapi import HTTPException
from app.api.services.car_service import CarService
from app.api.models.car import Car

# Controller class.
#
# This class is responsible for handling the requests and responses.
# It will call the service layer to get the data and return the response.
# It will also handle any exceptions that are raised by the service layer.


class CarController:
    def __init__(self, service: CarService):
        self._service = service

    def get_all(self):
        # Call the service to get the cars.
        pass

    def get_by_id(self, car_id: int):
        pass

    def create(self, car_data: Car):
        pass

    def update(self, car_id: int, car_data: Car):
        pass

    def delete(self, car_id: int):
        pass
