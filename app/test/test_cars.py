import pytest
from os import environ
from fastapi.testclient import TestClient
from app.api.models.veiculo import Veiculo
from app.main import app


# This fixture will be executed before each test.
# It will create a TestClient instance and pass it to the test function.
# The test function will be able to send requests to the application.
@pytest.fixture(scope="module")
def test_app():
    # Set the MOCK_DATABASE environment variable to True.
    # This will make the get_database() function return a mocked database.
    environ["MOCK_DATABASE"] = "true"
    yield TestClient(app)


# def test_create_car(test_app: TestClient):
#     # Send a POST request to the /cars endpoint.
#     # The request body represents a car object.
#     veiculo_data = Veiculo(
#         id="1",
#         name="Fiat Uno",
#         description="Small and cheap car."
#     )
#     response = test_app.post("/veiculos", json=veiculo_data.dict())
#     # Assert that the response status code is 200, for example.
#     assert response.status_code == 200
#     # Assert more things as needed...
