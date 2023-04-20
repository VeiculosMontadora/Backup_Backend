from app.api.models.veiculo import Veiculo
from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult

# CarRepository class
#
# This class is responsible for accessing the database to get the cars.
# It will be called by the service layer to get the data.
# It will also handle any exceptions that are raised by the database.

VEICULO_COLLECTION = "Veiculos"


class VeiculoRepository:
    def __init__(self, database: Database):
        self._collection = database[VEICULO_COLLECTION]

    def get_all(self) -> list[Veiculo]:
        veiculos = []
        veiculos_dict = list(self._collection.find())
        for veiculo in veiculos_dict:
            veiculos.append(Veiculo.parse_obj(veiculo))
        return veiculos

    def get_by_sigla(self, sigla: str) -> Veiculo:
        veiculo_dict = self._collection.find_one({"sigla": sigla})
        return Veiculo.parse_obj(veiculo_dict)
        

    def create(self, veiculo_data: Veiculo):
        # On create we need to convert car_data to dict and then insert it into the database.
        # Ex: db.insert_one(car_data.dict())
        self._collection.insert_one(veiculo_data.dict())

    def update(self, sigla: int, veiculo_data: Veiculo) -> UpdateResult:
        return self._collection.update_one({"sigla": sigla}, {"$set": veiculo_data.dict()})

    def delete(self, sigla: int) -> DeleteResult:
        return self._collection.delete_one({"sigla": sigla})
