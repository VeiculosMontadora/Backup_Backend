from pydantic import BaseModel
from typing import List


# Most fields are optional because there will be times when it will not
# be possible to get all the information. It will depend on how the pdf
# extraction is done.


class Combustivel(BaseModel):
    potencia: str = ""
    tipo_combustivel: str = ""


class Motor(BaseModel):
    cilindradas: str = ""
    nro_cilindradas: str = ""
    combustiveis: List[Combustivel] = []


class Veiculo(BaseModel):
    desc_cat: str = ""
    renavam_desc: str = ""
    sigla: str  # Required.
    pacote_def_modelo: str = ""
    versao: str = ""
    ano: str = ""
    marca: str = ""
    linha: str = ""
    motor: Motor = Motor()
    carga: str = ""
    num_passag: str = ""
    num_portas: str = ""
    num_renavam: str = ""
    status: str = "PENDENTE"
    producao: str = ""
    desc_vendas: str = ""
    pdf_names: List[str] = []
