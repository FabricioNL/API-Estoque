from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    title: str = Field(title="O título do item", max_length=30, example="Cadeira")
    description: str = Field(title="A descrição do item", max_length=100, example="Cadeira de escritório")
    price: float = Field(title="O preço do item", gt=0, example=100.00)
    
class ItemCreate(ItemBase):
    pass

class ItemUpdateQuantidade(BaseModel):
    qtd: int = Field(title="A quantidade a ser adicionada ou removida do item", example=10)
    
class ItemUpdateSituacao(BaseModel):
    is_active: bool = Field(title="A situação do item", example=True, default=True)

class Item(ItemBase):
    id: int
    is_active: bool = Field(default=True)
    qtd: int = Field(default = 0)

    class Config:
        orm_mode = True

class MovimentacaoBase(BaseModel):
    qtd: int = Field(title="A quantidade a ser adicionada ou removida do item", example=10)
    item_id: int = Field(title="O id do item", example=1)
    resume: str = Field(title="O resumo da movimentação", max_length=100, example="Quantidade do item Cadeira (id = 2) atualizada em 10")

class MovimentacaoCreate(MovimentacaoBase):
    pass

class Movimentacao(MovimentacaoBase):
    id: int

    class Config:
        orm_mode = True

class Message(BaseModel):
    info : str = Field(title="A mensagem de retorno", example="Item deletado com sucesso")
