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
        return self._repository.get_all()

    def get_by_sigla(self, sigla: str) -> Veiculo:
        try:
            return self._repository.get_by_sigla(sigla)
        except Exception:
            raise HTTPException(
                status_code=404, detail="Veiculo nao encontrado.")

    def create(self, veiculo_data: Veiculo) -> Veiculo:
        result = self._repository.create(veiculo_data)
        return self._repository.find_by_id(result.inserted_id)

    def update(self, sigla: str, veiculo_data: Veiculo) -> Veiculo:
        result = self._repository.update(sigla, veiculo_data)
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400, detail="Nenhum dado encontrado ou modificado.")
        return self._repository.get_by_sigla(sigla)

    def delete(self, sigla: str) -> str:
        result = self._repository.delete(sigla)
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=400, detail="Dado nao encontrado para deletar.")
        return sigla
