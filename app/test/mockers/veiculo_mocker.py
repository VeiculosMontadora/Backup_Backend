from app.api.models.veiculo import Combustivel, Motor, Veiculo


# This function will return a Veiculo instance with mocked data.
def mock_veiculo_with_default_params() -> Veiculo:
    return Veiculo(
        desc_cat="desc",
        renavam_desc="renavam",
        sigla="1234Test",
        pacote_def_modelo="pacote",
        versao="versao",
        ano="ano",
        marca="marca",
        linha="linha",
        motor=Motor(
            cilindradas="cilindradas",
            nro_cilindradas="nro_cilindradas",
            combustiveis=[Combustivel(
                potencia="potencia", tipo_combustivel="tipo_combustivel")]
        ),
        carga="carga",
        num_passag="num_passag",
        num_portas="num_portas",
        num_renavam="num_renavam",
        status="status",
        pdf_names=["pdf_names"]
    )
