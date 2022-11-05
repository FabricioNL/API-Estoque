from tkinter import CASCADE
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship, backref

from database import Base

class Movimentacao(Base):
    __tablename__ = "movimentacao"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    qtd = Column(Integer)
    resume = Column(String(100), index = True)
    owner = relationship("Item", back_populates="movimentacoes")
     
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    qtd = Column(Integer, index=True, default=0)
    description = Column(String(100), index=True)
    price = Column(Float, index=True)
    is_active = Column(Boolean, default=True)
    movimentacoes = relationship("Movimentacao", back_populates="owner", cascade="all, delete-orphan")