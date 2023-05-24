from datetime import date
from io import BytesIO
from app.api.models.veiculo import Copiavel, Veiculo, Motor, Combustivel
from app.pdf.chevrolet.ChevroletPDFReader import ChevroletPDFReader
from app.pdf.jeep.JeepPDFReader import JeepPDFReader
from fastapi import HTTPException
from typing import List
from app.api.models.pdf import PDF, Status
from app.api.repositories.pdf_repository import PDFRepository
from app.utils.utils import current_date


CHEVROLET_MONTADORA = "chevrolet"
JEEP_MONTADORA = "jeep"


class PDFService:
    def __init__(self, repository: PDFRepository):
        self._repository = repository

    def get_all(self) -> List[PDF]:
        return self._repository.get_all()

    def get_by_nome(self, nome: str) -> PDF:
        try:
            return self._repository.get_by_nome(nome)
        except Exception as error:
            raise HTTPException(
                status_code=404, detail=error.args[0])

    def create(self, pdf_data: PDF) -> PDF:
        # Set date attributes.
        created_date = current_date()
        pdf_data.criado = created_date
        pdf_data.ultimo_visto = created_date
        result = self._repository.create(pdf_data)
        return self._repository.find_by_id(result.inserted_id)

    def update(self, nome: str, pdf_data: PDF) -> PDF:
        pdf_data.ultimo_visto = current_date()
        result = self._repository.update(nome, pdf_data)
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400, detail="Nenhum dado encontrado ou modificado.")
        return self._repository.get_by_nome(nome)

    def update_veiculo(self, nome: str, sigla: str, veiculo_date: Veiculo) -> None:
        result = self._repository.update_veiculo(nome, sigla, veiculo_date)
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400, detail="Nenhum dado encontrado ou modificado.")

    def update_pdf_status(self, nome: str, status: Status) -> None:
        result = self._repository.update_pdf_status(nome, status)
        if result.modified_count == 0:
            raise HTTPException(
                status_code=400, detail="Nenhum dado encontrado ou modificado.")

    def delete(self, nome: str) -> str:
        result = self._repository.delete(nome)
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=400, detail="Dado não encontrado para deletar.")
        return nome

    # This function will create a Veiculo object using the data read from a PDF file.
    # It redirects the call to the correct function based on the 'montadora' parameter.
    def create_by_pdf(self, file_name: str, pdf_bytes: bytes, montadora: str) -> PDF:
        if str.lower(montadora) == CHEVROLET_MONTADORA:
            return self._create_by_pdf_chevrolet(file_name, pdf_bytes)
        elif str.lower(montadora) == JEEP_MONTADORA:
            return self._create_by_pdf_jeep(file_name, pdf_bytes)
        else:
            raise HTTPException(
                status_code=400, detail="Montadora inválida.")

    # This function will create a Veiculo object using the data read from a PDF file.
    # It is specific for Chevrolet PDFs.
    def _create_by_pdf_chevrolet(self, file_name: str, pdf_bytes: bytes) -> PDF:
        # BytesIO is used to read the PDF bytes.
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
                    # Data of the column with name 85% similar to 'CÓDIGO VENDAS' will be stored in the 'sigla' key.
                    ("CÓDIGO VENDAS", 85): "sigla",
                    ("DESCRIÇÃO VENDAS", 85): "desc_vendas",
                    ("MARCA/MODELO", 50): "num_renavam",
                    ("DESCRIÇÃO NO CAT", 85): "desc_cat",
                    ("PRODUÇÃO", 85): "producao",
                })
                vehicles_data.append(line_data)

        # List of vehicles to be added in the PDF response.
        vehicles = []
        for vehicle_dict in vehicles_data:
            # Setting the data from the PDF to the Veiculo object.
            sigla = vehicle_dict["sigla"]
            desc_cat = vehicle_dict["desc_cat"]
            num_renavam = vehicle_dict["num_renavam"]
            producao = vehicle_dict["producao"]
            desc_vendas = vehicle_dict["desc_vendas"]
            vehicle = Veiculo(
                sigla=Copiavel(valor=sigla),
                desc_cat=Copiavel(valor=desc_cat),
                num_renavam=Copiavel(valor=num_renavam),
                producao=Copiavel(valor=producao),
                desc_vendas=Copiavel(valor=desc_vendas)
            )
            vehicles.append(vehicle)

        # Creating the PDF object.
        pdf = PDF(
            nome=file_name,
            veiculos=vehicles
        )
        new_pdf = self.create(pdf)

        # Returning the PDF created.
        return new_pdf

    # This function will create a Veiculo object using the data read from a PDF file.
    # It is specific for JEEP PDFs.
    def _create_by_pdf_jeep(self, file_name: str, pdf_bytes: bytes) -> PDF:
        # BytesIO is used to read the PDF bytes.
        bytes_io = BytesIO(pdf_bytes)

        # Instantiating the PDF reader.
        pdf_reader = JeepPDFReader(pdf_bytes=bytes_io)

        # List of vehicles to be added in the PDF response.
        vehicles = []

        vehicles_data = pdf_reader.get_cars()
        for key in vehicles_data:
            # Getting the data read from the PDF.
            vehicle_dict = vehicles_data[key]
            sigla = vehicle_dict["sigla"]
            desc_cat = vehicle_dict["desc_cat"]
            desc_renavam = vehicle_dict["desc_renavam"]
            motor = ""
            # Just in case the motor could not be read from the PDF.
            if "motor" in vehicle_dict:
                motor = vehicle_dict["motor"]
            linha = vehicle_dict["linha"]
            marca = vehicle_dict["marca"]
            ano = vehicle_dict["ano"]
            potencia = vehicle_dict["potencia"]
            combustivel = vehicle_dict["combustivel"]
            preco = vehicle_dict["preco"]

            # Creating the Veiculo object.
            vehicle = Veiculo(
                sigla=Copiavel(valor=sigla),
                desc_cat=Copiavel(valor=desc_cat),
                desc_renavam=Copiavel(valor=desc_renavam),
                linha=Copiavel(valor=linha),
                marca=Copiavel(valor=marca),
                ano=Copiavel(valor=ano),
                preco=Copiavel(valor=f'R${preco}'),
                motor=Motor(
                    modelo=Copiavel(valor=motor),
                    combustiveis=[
                        Combustivel(
                            tipo_combustivel=Copiavel(valor=combustivel),
                            potencia=Copiavel(valor=potencia)
                        )
                    ],
                )
            )

            # Appending the Veiculo object to the list.
            vehicles.append(vehicle)

        # Creating the PDF object.
        pdf = PDF(
            nome=file_name,
            veiculos=vehicles
        )
        new_pdf = self.create(pdf)

        # Returning the PDF created.
        return new_pdf
