# from fastapi import HTTPException
from app.api.services.veiculo_service import VeiculoService
from app.api.models.veiculo import Veiculo

# Controller class.
#
# This class is responsible for handling the requests and responses.
# It will call the service layer to get the data and return the response.
# It will also handle any exceptions that are raised by the service layer.


class VeiculoController:
    def __init__(self, service: VeiculoService):
        self._service = service

    def get_all(self) -> list[Veiculo]:
        return self._service.get_all()

    def get_by_sigla(self, sigla: str) -> Veiculo:
        return self._service.get_by_sigla(sigla)

    def create(self, veiculo_data: Veiculo) -> None:
        self._service.create(veiculo_data)

    def update(self, sigla: int, veiculo_data: Veiculo) -> None:
        self._service.update(sigla, veiculo_data)

    def delete(self, sigla: int) -> None:
        self._service.delete(sigla)
