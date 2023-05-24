from app.api.models.veiculo import Veiculo
from bson import ObjectId
from pymongo.database import Database
from pymongo.results import UpdateResult, DeleteResult, InsertOneResult
from app.api.models.pdf import PDF, Status
from app.utils.utils import is_date_after

PDF_COLLECTION = "pdfs"


class PDFRepository:
    def __init__(self, database: Database):
        self._collection = database[PDF_COLLECTION]

    def get_all(self) -> list[PDF]:
        pdfs = []
        pdfs_dict = list(self._collection.find())
        for pdf in pdfs_dict:
            pdfs.append(PDF.parse_obj(pdf))
        return pdfs

    def get_by_nome(self, nome: str) -> PDF:
        # This method returns the latest pdf with the given nome.
        # It uses the 'criado' field to determine which pdf is the latest.
        all_pdfs = self.get_all()
        latest_pdf = None
        for pdf in all_pdfs:
            if pdf.nome == nome:
                if latest_pdf is None:
                    latest_pdf = pdf
                else:
                    if is_date_after(pdf.criado, latest_pdf.criado):
                        latest_pdf = pdf
        if latest_pdf is None:
            raise Exception(f"PDF com nome {nome} não encontrado.")
        return latest_pdf

    def create(self, pdf_data: PDF) -> InsertOneResult:
        # On create we need to convert car_data to dict and then insert it into the database.
        # Ex: db.insert_one(car_data.dict())
        return self._collection.insert_one(pdf_data.dict())

    def update(self, nome: str, pdf_data: PDF) -> UpdateResult:
        print(pdf_data)
        return self._collection.update_one({"nome": nome}, {"$set": pdf_data.dict()})
    
    def update_veiculo(self, nome_pdf: str, sigla_veiculo: str, veiculo_data: Veiculo) -> UpdateResult:
        return self._collection.update_one({"nome": nome_pdf, "veiculos": {"$elemMatch":{"sigla.valor": sigla_veiculo}}}, {"$set": {"veiculos.$": veiculo_data.dict()}})
    
    def update_pdf_status(self, nome_pdf: str, status: Status) -> UpdateResult:
        return self._collection.update_one({"nome": nome_pdf}, {"$set": {"status": status}})

    def delete(self, nome: str) -> DeleteResult:
        return self._collection.delete_one({"nome": nome})

    def find_by_id(self, pdf_id: ObjectId):
        pdf_dict = self._collection.find_one({"_id": pdf_id})
        return PDF.parse_obj(pdf_dict)
