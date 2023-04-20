from pydantic import BaseModel


class Combustivel(BaseModel):
    potencia: str
    tipo_combustivel: str


class Motor(BaseModel):
    cilindradas: str
    nro_cilindradas: str
    combustiveis: list[Combustivel]


class Veiculo(BaseModel):
    desc_cat: str
    renavam_desc: str
    sigla: str
    pacote_def_modelo: str
    versao: str
    ano: str
    marca: str
    linha: str
    motor: Motor
    carga: str
    num_passag: str
    num_portas: str
    num_renavam: str
    status: str
    pdf_names: list[str]
