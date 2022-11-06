from sqlalchemy.orm import Session

import models, schemas

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_movimentacoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movimentacao).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    
    print(item)
    
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"info": "item deletado com sucesso"}

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    
    if db_item.is_active == False:
        return None
    
    db_item.title = item.title
    db_item.description = item.description
    db_item.price = item.price
    
    db.commit()
    db.refresh(db_item)
    return db_item

def update_quantidade_item(db: Session, item_id: int, item: schemas.ItemUpdateQuantidade):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    
    if db_item.is_active == False:
        return None
    
    db_item.qtd = item.qtd + db_item.qtd 
    
    if db_item.qtd < 0:
        return None
    
    movimentacao = schemas.MovimentacaoBase(qtd = item.qtd, item_id = item_id, resume = "Quantidade do item {0} (id = {1}) atualizada em {2}".format(db_item.title, db_item.id, item.qtd))
    create_movimentacao(db, movimentacao)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def update_situacao_item(db: Session, item_id: int, item: schemas.ItemUpdateSituacao):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    
    db_item.is_active = item.is_active
    
    db.commit()
    db.refresh(db_item)
    return db_item

def create_movimentacao(db: Session, movimentacao: schemas.MovimentacaoCreate):
    
    db_movimentacao = models.Movimentacao(**movimentacao.dict())
    db.add(db_movimentacao)
    db.commit()
    db.refresh(db_movimentacao)
    return db_movimentacao

