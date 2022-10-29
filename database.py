from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os

load_dotenv()

SQL_SERVER=os.getenv("SQL_SERVER")
SQL_USER=os.getenv("SQL_USER")
SQL_PASSWORD=os.getenv("SQL_PASSWORD")
SQL_DB=os.getenv("SQL_DB")
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

SQLALCHEMY_DATABASE_URL=f"mysql+mysqlconnector://{SQL_USER}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DB}"
print("HERE -> ", SQLALCHEMY_DATABASE_URL)

print("Criando engine")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

if not database_exists(engine.url):
    create_database(engine.url)

print("Iniciando sessão local")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
