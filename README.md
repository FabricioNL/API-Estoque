# API-Estoque

## Nome dos integrantes do grupo: 

**Fabricio Neri Lima**

**Jean Silas Sanandrez**

## Proposta do projeto:

Uma API Rest para gerenciamento de um estoque feita com Fast API. Além da API, foi realizada uma documentação por meio do swagger.

## Como testar:

Basta clonar o repositório e dentro da pasta pelo cmd, inserir o comando ```uvicorn main:app --reload```. Ele permitirá que você teste a API localmente no http://127.0.0.1:8000.

Para acessar a documentação, também é preciso iniciar o script pelo comando e entã acessar pelo navegador ```http://127.0.0.1:8000/redoc``` ou ```http://127.0.0.1:8000/doc```

## Parte 2:

Para a parte 2, o projeto foi dividido em vários arquivos, como:

- crud.py
- database.py
- main.py
- models.py
- schemas.py

É importante que todos os salvamentos envolvem variáveis de ambiente, então é preciso que crie um arquivo .env com as variaveis necessárias para testar.

