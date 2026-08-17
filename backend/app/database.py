import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

def get_engine(dbname: str = None):
    
    if dbname is None:
        dbname = os.getenv("DB_NAME")

    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    return create_engine(DATABASE_URL, echo=False)

engine = get_engine()

def veritabani_hazirla(dbname: str = None):

    if dbname:
        SQLModel.metadata.create_all(get_engine(dbname))
    else:
        SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session        