from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#cria um item relacionado a um usuario
@app.post("/items/", response_model=schemas.Item, summary="Cria item",status_code=status.HTTP_201_CREATED)
def create_item_for_user(
    item: schemas.ItemCreate, db: Session = Depends(get_db)):
    
    """
    Cria um item com todas as informações:
    
    Args:
    
        Item (Item): Um item com informações como **Nome**, **Preco**, **Descricao**
    
    Retorno:
    
        Item: Retorna o item que foi adicionado no banco de dados
    """
    
    return crud.create_item(db=db, item=item)

#atualiza um item
@app.put("/item/{item_id}/", response_model=schemas.Item, 
         summary="Atualiza item", status_code=status.HTTP_200_OK)
def update_item(
    item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Atualiza as caracteristicas do item, como nome, descrição e preço.
    
    Args:
    
        item_id (int):  id relacionado a um item da base de dados
        item (ItemUpdate): um json com o nome, descrição e preço do item
    
    Exceções:
    
        HTTPException: o item está desativado. Para atualizar o item, ative-o primeiro. 
        
    Retorno:
    
        um item com a quantidade atualizada (adicionada ou removida)
        
    """
    result = crud.update_item(db=db, item=item, item_id=item_id)

    if result == None:
        raise HTTPException(status_code=404, detail="Item não pode ser atualizado pois está inativo")
    
    return result
    
#atualiza a quantidade de um item
@app.put("/item/quantidade/{item_id}/", response_model=schemas.Item, 
         summary="Atualiza quantidade do item", status_code=status.HTTP_200_OK)
def update_item(
    item_id: int, item: schemas.ItemUpdateQuantidade, db: Session = Depends(get_db)):
    """
    Atualiza a quantidade de um item cadastrado no banco de dados
    
    Args:
    
        item_id (int):  id relacionado a um item da base de dados
        item (ItemUpdateQuantidade): um json com a quantidade a ser adicionada ou removida do item
    
    Exceções:
    
        HTTPException: o item não existe ou a quantidade a ser removida 
        é maior que a quantidade atual do item
        
    Retorno:
    
        um item com a quantidade atualizada (adicionada ou removida)
        
    """
    
    result = crud.update_quantidade_item(db=db, item=item, item_id=item_id)
    if result == None:
        raise HTTPException(status_code=404, detail="Item não pode ser atualizado pois está inativo ou a quantidade tornou o estoque negativo")
    
    return result
    
#atualiza a situacao de um item
@app.put("/item/situacao/{item_id}/", response_model=schemas.Item, 
         summary="Atualiza a situação do item", status_code=status.HTTP_200_OK)
def update_item(
    item_id: int, item: schemas.ItemUpdateSituacao, db: Session = Depends(get_db)):
    
    """
    Atualiza a situação cadastral do item. Caso você não trabalhe mais com o item,
    não o exclua, apenas desative-o. Isso é importante para que você possa manter
    as movimentações do item casa reativi-o.
    
    Args:
    
        item_id (int):  id relacionado a um item da base de dados
        item (ItemUpdateSituacao): um json com a situação do item (false ou true)
         
    Retorno:
    
        um item com a quantidade situação atualizada (adicionada ou removida)
        
    """
    result = crud.update_situacao_item(db=db, item=item, item_id=item_id)
    if result == None:
        raise HTTPException(status_code=404, detail="Item não pode ser deletado pois o id não corresponde a nenhum item")
    
    return result
#deleta um item de um usuario
@app.delete("/item/{item_id}/", response_model=schemas.Message, summary="Deleta um item", status_code=status.HTTP_200_OK)
def delete_item(item_id: int = Path(title="O id correspondente ao item que deseja deletar", ge=0), db: Session = Depends(get_db)):
    """
    Deleta um item da base de dados que corresponda ao id desejado. Delete um item apenas caso
    tenha certeza que não irá mais trabalhar com ele. Caso contrário, apenas desative-o. Deletá-lo
    irá deletar suas movimentações.
    
    Args:
    
        item_id (int):  id relacionado a um item da base de dados
    
    Exceções:
    
        HTTPException: o id não corresponde a um item da base para ser deletado
        
    Retorno:
    
        info (str): Uma string informando que houve sucesso no 
        processo de delete do item desejado
    """
    return crud.delete_item(db=db, item_id=item_id)

#obtem todos os items
@app.get("/items/", response_model=list[schemas.Item], summary="Obtem todos os items", status_code=status.HTTP_200_OK)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

#obtem todos os items
@app.get("/movimentacoes/", response_model=list[schemas.Movimentacao], summary="Obtem todas as movimentações", status_code=status.HTTP_200_OK)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movimentacoes = crud.get_movimentacoes(db, skip=skip, limit=limit)
    return movimentacoes

