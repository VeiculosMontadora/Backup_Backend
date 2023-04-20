from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from fastapi import FastAPI, File, UploadFile
from app.api.models.veiculo import Veiculo
from app.database.mongo import get_database
from app.api.repositories.veiculo_repository import VeiculoRepository
from app.api.services.veiculo_service import VeiculoService
from app.api.controllers.veiculo_controller import VeiculoController


# Car router.
#
# Here we define the routes for the car resource.
# We call the CarController to handle the requests.

# These variables start with an underscore to indicate that they are 'private'.
# They are not meant to be used outside of this file.
_database = get_database()
_repository = VeiculoRepository(_database)
_service = VeiculoService(_repository)
_veiculo_controller = VeiculoController(_service)
_veiculo_router = APIRouter(prefix="/veiculos")


@_veiculo_router.get("/")
def get_veiculos() -> list[Veiculo]:
    return _veiculo_controller.get_all()


@_veiculo_router.get("/{sigla}")
def get_veiculo(sigla: str) -> Veiculo:
    return _veiculo_controller.get_by_sigla(sigla)


@_veiculo_router.post("/")
def create_veiculo(veiculo_data: Veiculo) -> None:
    _veiculo_controller.create(veiculo_data)


@_veiculo_router.put("/{sigla}")
def update_veiculo(sigla: str, veiculo_data: Veiculo) -> None:
    _veiculo_controller.update(sigla, veiculo_data)


@_veiculo_router.delete("/{sigla}")
def delete_veiculo(sigla: str) -> None:
    _veiculo_controller.delete(sigla)

# It contains a single endpoint that receives the PDF file.
@_veiculo_router.post("/pdf/")
def create_upload_file(form_data: UploadFile = File(...)):
    contents = form_data.file.read() # This function read the pdf bytes.
    contents # Here we have the pdf bytes saved in the application memory. The ideia is to call a funtion which will handle the pdf bytes and extract them.

    name : str
    name = form_data.filename # This is the file name in memory. It will be used to save the veiculo JSON in the database.

    return {"filename": form_data.filename}

# This function is used to get the car router.
# It is used in the main.py file to include the router in the FastAPI app.
def get_veiculo_router() -> APIRouter:
    return _veiculo_router
