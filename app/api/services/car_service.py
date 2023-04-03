from app.api.repositories.car_repository import CarRepository
from app.api.models.car import Car

# Service class.
#
# This class is responsible for handling the business logic.
# It will call the repository layer to get the data and return the response.
# It will also handle any exceptions that are raised by the repository layer.


class CarService:
    def __init__(self, repository: CarRepository):
        self._repository = repository

    def get_all(self):
        # Call the repository to get the cars.
        pass

    def get_by_id(self, car_id: int):
        pass

    def create(self, car_data: Car):
        pass

    def update(self, car_id: int, car_data: Car):
        pass

    def delete(self, car_id: int):
        pass
