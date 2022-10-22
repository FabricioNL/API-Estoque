from operator import gt
from fastapi import FastAPI, Path, Query, HTTPException, Body
from pydantic import BaseModel


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

@app.get("/item", 
        status_code=200, 
        tags=["items"],
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
        status_code=200, 
        tags=["items"],
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
        raise HTTPException(status_code=404, detail="Item not found")
    
    return items[item_id]


@app.put("/item/{item_id}", 
        tags=["items"],
        response_model=Item, 
        status_code=200, 
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
            raise HTTPException(status_code=404, detail="Item not found")
    
    items[item_id] = Item
    return Item 
    