from fastapi import HTTPException
from app.api.repositories.veiculo_repository import VeiculoRepository
from app.api.models.veiculo import Veiculo

# Service class.
#
# This class is responsible for handling the business logic.
# It will call the repository layer to get the data and return the response.
# It will also handle any exceptions that are raised by the repository layer.


class VeiculoService:
    def __init__(self, repository: VeiculoRepository):
        self._repository = repository

    def get_all(self) -> list[Veiculo]:
        # Call the repository to get the cars.
        return self._repository.get_all()

    def get_by_sigla(self, sigla: str) -> Veiculo:
        try: 
            return self._repository.get_by_sigla(sigla)
        except Exception as e:
            raise HTTPException(status_code=404, detail="Veiculo nao encontrado")

    def create(self, veiculo_data: Veiculo) -> None:
        self._repository.create(veiculo_data)

    def update(self, sigla: int, veiculo_data: Veiculo) -> None:
        response = self._repository.update(sigla, veiculo_data)
        if response.modified_count == 0:
            raise HTTPException(status_code=400, detail="Nenhum dado encontrado ou modificado")

    def delete(self, sigla: int) -> None:
        response = self._repository.delete(sigla)
        if response.deleted_count == 0:
            raise HTTPException(status_code=400, detail="Dado nao encontrado para deletar")
