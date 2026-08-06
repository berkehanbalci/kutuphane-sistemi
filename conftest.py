import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from database import get_engine, get_session
import models
import main

TEST_DB = "kutuphane_test_db"

if "test" not in TEST_DB:
    raise RuntimeError("Test veritabanı adında 'test' kelimesi geçmeli! Gerçek db koruması!")

test_engine = get_engine(TEST_DB)

def test_get_session():
    with Session(test_engine) as session:
        yield session

main.app.dependency_overrides[get_session] = test_get_session

@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture(autouse=True)
def temiz_veritabani():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield

@pytest.fixture
def token(client):
    client.post("/kayit", json={
        "kullanici_adi": "test_admin",
        "sifre": "test1234"
    })

    cevap = client.post("/giris", json={
        "kullanici_adi": "test_admin",
        "sifre": "test1234"
    })

    access_token = cevap.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}




