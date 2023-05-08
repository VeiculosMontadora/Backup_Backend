# Backend

Repositório do backend do projeto Veículos Via Montadora. O backend é desenvolvido em **Python** com o framework **FastAPI**. O banco de dados utilizado é o **MongoDB**. O projeto utiliza o **Poetry** para gerenciamento de dependências e **Pytest** para testes unitários. Além disso, o código deste repositório é executado em cima de uma função **AWS Lambda**.

## Requisitos

A seguir estão listados os requisitos para executar o projeto:

### Python ^3.9

Para instalar o Python, acesse o [site oficial](https://www.python.org/downloads/) e siga as instruções de instalação. Você deve instalar uma versão `> 3.9` (3.10.4 recomendada), caso o contrário, o projeto não irá funcionar.

Se você já tem o Python instalado, você pode verificar a versão com o seguinte comando:

```sh
python --version
```

Caso você tenha uma versão diferente da recomendada, você deve instalar a versão correta.

### Docker

Para instalar o Docker, acesse o [site oficial](https://docs.docker.com/get-docker/) e siga as instruções de instalação. A instalação do Docker pode ser um pouco complexa, então não hesite em procurar ajuda com membros mais experientes da equipe.

## Desenvolvimento

Agora que você tem o Python e o Docker instalados, você pode começar a trabalhar no projeto:

- Primeiro, clone o repositório do projeto:

```sh
git clone https://tools.ages.pucrs.br/veiculos-via-montadora/backend.git
```

- Em seguida, entre na pasta do projeto:

```sh
cd backend
```

### Servidor API - FastAPI

Para iniciar o servidor da API, siga as instruções abaixo:

- Instale o gerenciador de dependências **Poetry** na versão **1.4.1**:

```sh
pip install "poetry==1.4.1"
```

- Configure o Poetry para criar o ambiente virtual dentro da pasta do projeto:

```sh
poetry config virtualenvs.in-project true
```

- Agora instale as dependências do projeto:

```sh
poetry install
```

- Agora você pode iniciar o servidor localmente:

```sh
poetry run uvicorn app.main:app --reload
```

O servidor estará disponível em [http://localhost:8000](http://localhost:8000/).

### Banco de Dados - MongoDB

Você fará uso do Docker para executar o banco de dados MongoDB dentro de um container. Para isso, siga as instruções abaixo:

- Execute o comando abaixo para iniciar o container do MongoDB:

```sh
docker compose up mongodb
```

Isso irá iniciar o container do MongoDB em segundo plano. Para parar o container, execute o seguinte comando:

```sh
docker compose down
```

### Testes Unitários

Para executar os testes unitários da aplicação, execute o seguinte comando na raiz do projeto:

```sh
poetry run pytest
```
