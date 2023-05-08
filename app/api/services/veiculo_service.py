from io import BytesIO
from fastapi import HTTPException
from app.api.repositories.veiculo_repository import VeiculoRepository
from app.api.models.veiculo import Veiculo
from app.pdf.chevrolet.ChevroletPDFReader import ChevroletPDFReader


CHEVROLET_MONTADORA = "chevrolet"

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

    # This function will create a Veiculo object using the data read from a PDF file.
    # It redirects the call to the correct function based on the 'montadora' parameter.
    def create_by_pdf(self, file_name: str, pdf_bytes: bytes, montadora: str) -> Veiculo:
        if str.lower(montadora) == CHEVROLET_MONTADORA:
            return self._create_by_pdf_chevrolet(file_name, pdf_bytes)
        else:
            raise HTTPException(
                status_code=400, detail="Montadora inválida.")

    # This function will create a Veiculo object using the data read from a PDF file.
    # It is specific for Chevrolet PDFs.
    def _create_by_pdf_chevrolet(self, file_name: str, pdf_bytes: bytes) -> list[Veiculo]:
        bytes_io = BytesIO(pdf_bytes)

        # PDFs from 2023 tend to only work with the lattice mode on,
        # while PDFs from 2022 tend to only work with the lattice mode off.
        # This is for sure not a rule, it is what has been observed MOST of the time.
        # This is also a TERRIBLE way to do this, but there is no good way to do this.
        # Each PDF has its own way of being read, no patterns, and there is no way to know beforehand.
        #
        # From tabula-py documentation:
        #
        # "lattice: Force PDF to be extracted using lattice-mode extraction
        # (if there are ruling lines separating each cell, as in a PDF of an Excel spreadsheet)"
        lattice = True if '2023' in file_name else False
        pdf_reader = ChevroletPDFReader(bytes_io, lattice=lattice)

        # DEBUG: Print the PDF tables.
        # pdf_reader.print_tables()

        # Here we are reading the data from the first tables in the PDF.
        vehicles_data = []
        table_group = ChevroletPDFReader.INTRODUCTION_GROUP
        for i in range(pdf_reader.get_tables_count(table_group)):
            for j in range(pdf_reader.get_lines_count(table_group, i)):
                line_data = pdf_reader.get_line_values(table_group, i, j, {
                    # Data of the column with name 85% similar to 'CÓDIGO VENDAS' will be stored in the 'codigo_vendas' key.
                    ("CÓDIGO VENDAS", 85): "sigla",
                    ("DESCRIÇÃO VENDAS", 85): "desc_vendas",
                    ("MARCA/MODELO", 50): "num_renavam",
                    ("DESCRIÇÃO NO CAT", 85): "desc_cat",
                    ("PRODUÇÃO", 85): "producao",
                })
                vehicles_data.append(line_data)

        # List of vehicles to be returned by the API.
        vehicles = []
        for vehicle_dict in vehicles_data:
            # First we try to find the vehicle in the database using the 'sigla' as the search key.
            sigla = vehicle_dict["sigla"]
            vehicle_found = None
            try:
                vehicle_found = self.get_by_sigla(sigla)
                # Ok, found!
                # We will update the vehicle below.
            except:
                # Not found, no problem.
                # We will create the vehicle below.
                pass

            # Setting the data from the PDF to the Veiculo object.
            desc_cat = vehicle_dict["desc_cat"]
            num_renavam = vehicle_dict["num_renavam"]
            producao = vehicle_dict["producao"]
            desc_vendas = vehicle_dict["desc_vendas"]
            vehicle = Veiculo(sigla=sigla, desc_cat=desc_cat,
                              num_renavam=num_renavam, producao=producao, desc_vendas=desc_vendas)
            vehicle.status = "PROCESSADO"

            # If the vehicle was not found, we create a new one.
            # If the vehicle was found, we update it.
            if vehicle_found is None:
                vehicle.pdf_names = [file_name]
                new_vehicle = self.create(vehicle)
                vehicles.append(new_vehicle)
            else:
                vehicle.pdf_names = vehicle_found.pdf_names + [file_name]
                updated_vehicle = self.update(sigla, vehicle)
                vehicles.append(updated_vehicle)

        # Returning the list of vehicles.
        return vehicles

    # This function will create a Veiculo object using the data read from a PDF file.
    # It is specific for Jeep PDFs.
    # (NOT IMPLEMENTED YET)
    def _create_by_pdf_jeep(self, file_name: str, pdf_bytes: bytes) -> Veiculo:
        pass
