import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.test.mockers.pdf_mocker import build_pdf_with_default_params
from app.api.models.pdf import Status


# This fixture will be executed before each test.
# It will create a TestClient instance and pass it to the test function.
# The test function will be able to send requests to the application.
@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app=app)


# PDF Mock data.
pdf_data = build_pdf_with_default_params()


# Test cases.
def test_create_pdf(test_app: TestClient):
    response = test_app.post("/pdfs", json=pdf_data.dict())
    assert response.status_code == status.HTTP_200_OK


def test_get_all_pdfs(test_app: TestClient):
    response = test_app.get("/pdfs")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_pdf_by_nome(test_app: TestClient):
    nome = pdf_data.nome
    response = test_app.get(f"/pdfs/{nome}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == nome


def test_update_pdf_by_nome(test_app: TestClient):
    pdf_data.status = Status.CONCLUIDO
    nome = pdf_data.nome
    response = test_app.put(f"/pdfs/{nome}", json=pdf_data.dict())
    assert response.status_code == status.HTTP_200_OK


def test_delete_pdf_by_nome(test_app: TestClient):
    nome = pdf_data.nome
    response = test_app.delete(f"/pdfs/{nome}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == nome


def test_get_pdf_by_nome_not_found(test_app: TestClient):
    nome = pdf_data.nome
    response = test_app.get(f"/pdfs/{nome}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
