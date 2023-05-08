from fastapi import APIRouter, File, Form, UploadFile
from app.api.models.veiculo import Veiculo
from app.database.mongo import get_database
from app.api.repositories.veiculo_repository import VeiculoRepository
from app.api.services.veiculo_service import VeiculoService

# Car router.
#
# Here we define the routes for the car resource.
# This router also acts as the controller for the car resource.
# It receives the requests, calls the service and returns the response.

# These variables start with an underscore to indicate that they are 'private'.
# They are not meant to be used outside of this file.
_database = get_database()
_repository = VeiculoRepository(_database)
_veiculo_service = VeiculoService(_repository)
_veiculo_router = APIRouter(prefix="/veiculos")


## Routes - START ##

@_veiculo_router.get("/")
def get_veiculos() -> list[Veiculo]:
    return _veiculo_service.get_all()


@_veiculo_router.get("/{sigla}")
def get_veiculo(sigla: str) -> Veiculo:
    return _veiculo_service.get_by_sigla(sigla)


@_veiculo_router.post("/")
def create_veiculo(veiculo_data: Veiculo) -> Veiculo:
    return _veiculo_service.create(veiculo_data)


@_veiculo_router.put("/{sigla}")
def update_veiculo(sigla: str, veiculo_data: Veiculo) -> Veiculo:
    return _veiculo_service.update(sigla, veiculo_data)


@_veiculo_router.delete("/{sigla}")
def delete_veiculo(sigla: str) -> str:
    return _veiculo_service.delete(sigla)


@_veiculo_router.post("/upload/pdf")
def create_veiculo_by_pdf(file: UploadFile = File(...), montadora: str = Form(...)):
    pdf_bytes = file.file.read()
    file_name = file.filename
    return _veiculo_service.create_by_pdf(file_name, pdf_bytes, montadora)


## Routes - END ##


# This function is used to get the car router.
# It is used in the main.py file to include the router in the FastAPI app.
def get_veiculo_router() -> APIRouter:
    return _veiculo_router
