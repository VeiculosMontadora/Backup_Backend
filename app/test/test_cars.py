import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.test.mockers.veiculo_mocker import mock_veiculo_with_default_params


# This fixture will be executed before each test.
# It will create a TestClient instance and pass it to the test function.
# The test function will be able to send requests to the application.
@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app=app)


# Veiculo Mock data.
veiculo_data = mock_veiculo_with_default_params()


# Test cases.
def test_create_car(test_app: TestClient):
    response = test_app.post("/veiculos", json=veiculo_data.dict())
    assert response.status_code == status.HTTP_200_OK


def test_get_all_veiculos(test_app: TestClient):
    response = test_app.get("/veiculos")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_veiculo_by_sigla(test_app: TestClient):
    sigla = veiculo_data.sigla
    response = test_app.get(f"/veiculos/{sigla}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["sigla"] == sigla


def test_update_veiculo_by_sigla(test_app: TestClient):
    veiculo_data.ano = "2023"
    sigla = veiculo_data.sigla
    response = test_app.put(f"/veiculos/{sigla}", json=veiculo_data.dict())
    assert response.status_code == status.HTTP_200_OK


def test_delete_veiculo_by_sigla(test_app: TestClient):
    sigla = veiculo_data.sigla
    response = test_app.delete(f"/veiculos/{sigla}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == sigla


def test_get_veiculo_by_sigla_not_found(test_app: TestClient):
    sigla = veiculo_data.sigla
    response = test_app.get(f"/veiculos/{sigla}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
