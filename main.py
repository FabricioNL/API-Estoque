from operator import gt
from fastapi import FastAPI, Path, Query, HTTPException, Body, status
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from enum import Enum



app = FastAPI()

#exemplo de base de dados
items = [
    {"nome": "Foo", "preco": 50.2},
    {"nome": "Bar", "descricao": "The bartenders", "preco": 62},
    {"nome": "Baz", "descricao": None, "preco": 50.2,  "tags": []}
]

#classe para ITEM
class Item(BaseModel):
    nome: str
    descricao: str | None = None
    preco: float 
    tags: list[str] = []

#classe para o ESTOQUE
class Estoque(BaseModel):
    tamanho: int
    estoque: list[Item]

#classe para Mensagem
class Message(BaseModel):
    info : str

class Tags(Enum):
    items:str = "Items"
    inventario:str = "Inventário"
    
#decoretor para exception handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return await request_validation_exception_handler(request, exc)

@app.get("/item", 
        status_code=status.HTTP_200_OK, 
        tags=[Tags.inventario],
        summary="Obtem todos os itens",
        response_model=Estoque
)
async def get_itens():
    """
    Retorna um dicionario com duas chaves, uma sendo a quantidade de itens diferentes cadastrados 
    e outra uma lista com os itens.

    Formato:
        {
            "tamanho": int,
            "itens"  : list
        }
    
    Exemplo:

        {
            "tamanho": 3,
            "estoque": [
                {
                    "nome": "Flor de lótus",
                    "preco": 50.2
                },
                {
                    "nome": "Chá preto",
                    "descricao": "Chá preto importado da China",
                    "preco": 62
                },
                {
                    "nome": "Canela",
                    "descricao": "Canela em pau,
                    "preco": 20,
                    "tags": ["Importado", "Especiarias", "Tempero", "Em natura"]
                }
            ]
        }
            
    """
    
    return  {"quantidade": len(items), "itens": items}


@app.get("/item/{item_id}", 
        response_model=Item, 
        status_code=status.HTTP_200_OK, 
        tags=[Tags.items],
        summary="Obtem um item específico",
)
async def get_item(item_id: int = Path(title="O id correspondente ao item obter", ge=0)):
    """
    Retorna um dicionario com apenas o item requisitado e o seu id relacionado.

    Argumentos:
    
        item_id (int): id do item cadastrado

    Exceções:
    
        HTTPException: O item relacionado ao id fornecido não existe

    Retorno:
    
        Item: retorna um item com nome, preço, 
        além da descrição e tags relacionadas, caso possua
    """
    if item_id >= len(items):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    return items[item_id]


@app.put("/item/{item_id}", 
        tags=[Tags.items],
        response_model=Item, 
        status_code=status.HTTP_200_OK, 
        summary="Atualiza um item",
)
async def update_item(Item: Item,
    item_id: int = Path(title="O id correspondente ao item que deseja atualizar", ge=0)
    ):
    """
    Atualiza as informações relacionadas a um item com o id desejado
    
    Args:
    
        item_id (int): id relacionado a um item da base de dados

    Exceções:
    
        HTTPException: o id não corresponde a um item da base para ser atualizado

    Retorno:
    
        Item: o item que foi atualizado
    """
    
    if item_id >= len(items):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    items[item_id] = Item
    return Item 


@app.delete("/item/{item_id}", 
        status_code=status.HTTP_200_OK, 
        tags=[Tags.items],
        summary="Deleta um item",
        response_model=Message,
)
async def delete_item(item_id: int = Path(title="O id correspondente ao item que deseja deletar", ge=0)):
    """
    Deleta um item da base de dados que corresponda ao id desejado
    
    Args:
    
        item_id (int):  id relacionado a um item da base de dados

    Exceções:
    
        HTTPException: o id não corresponde a um item da base para ser deletado
        
    Retorno:
    
        info (str): Uma string informando que houve sucesso no 
        processo de delete do item desejado
    """
    if item_id >= len(items):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    del items[item_id]
    return {"info": "o item foi deletado com sucesso"}
    


@app.post("/item", 
        status_code=status.HTTP_201_CREATED, 
        tags=[Tags.items],
        summary="Cria um item",
        response_model=Item, 
)
async def create_item(Item: Item):
    """
    Cria um item com todas as informações:

    Args:
    
        Item (Item): Um item com informações como **Nome**, **Preco**, 
        **Descricao** e uma lista de **Tags**

    Retorno:
    
        Item: Retorna o item que foi adicionado no banco de dados
    """
    items.append(Item)

    return Item
    