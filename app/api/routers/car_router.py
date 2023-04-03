from fastapi import APIRouter
from app.api.models.car import Car
from app.database.mongo import get_database
from app.api.repositories.car_repository import CarRepository
from app.api.services.car_service import CarService
from app.api.controllers.car_controller import CarController

# Car router.
#
# Here we define the routes for the car resource.
# We call the CarController to handle the requests.

# These variables start with an underscore to indicate that they are 'private'.
# They are not meant to be used outside of this file.
_database = get_database()
_repository = CarRepository(_database)
_service = CarService(_repository)
_car_controller = CarController(_service)
_car_router = APIRouter(prefix="/cars")


@_car_router.get("/")
def get_cars():
    return _car_controller.get_all()


@_car_router.get("/{car_id}")
def get_car(car_id: str):
    return _car_controller.get_by_id(car_id)


@_car_router.post("/")
def create_car(car_data: Car):
    _car_controller.create(car_data)


@_car_router.put("/{car_id}")
def update_car(car_id: str, car_data: Car):
    return _car_controller.update(car_id, car_data)


@_car_router.delete("/{car_id}")
def delete_car(car_id: str):
    return _car_controller.delete(car_id)


# This function is used to get the car router.
# It is used in the main.py file to include the router in the FastAPI app.
def get_car_router() -> APIRouter:
    return _car_router
