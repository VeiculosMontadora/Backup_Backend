from bson import ObjectId
from app.api.models.veiculo import Veiculo
from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult, InsertOneResult


VEICULO_COLLECTION = "Veiculos"


# CarRepository class
#
# This class is responsible for accessing the database to get the cars.
# It will be called by the service layer to get the data.
# It will also handle any exceptions that are raised by the database.
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

    def create(self, veiculo_data: Veiculo) -> InsertOneResult:
        # On create we need to convert car_data to dict and then insert it into the database.
        # Ex: db.insert_one(car_data.dict())
        return self._collection.insert_one(veiculo_data.dict())

    def update(self, sigla: str, veiculo_data: Veiculo) -> UpdateResult:
        return self._collection.update_one({"sigla": sigla}, {"$set": veiculo_data.dict()})

    def delete(self, sigla: str) -> DeleteResult:
        return self._collection.delete_one({"sigla": sigla})

    def find_by_id(self, id: ObjectId):
        return Veiculo.parse_obj(self._collection.find_one({"_id": id}))
