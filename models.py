from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date

class Yonetici(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kullanici_adi: str = Field(unique=True)
    sifre_hash: str

class Yazar(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ad: str
    soyad:str

    kitaplar: List["Kitap"] = Relationship(back_populates="yazar")

class Kitap(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    baslik: str
    stok_adedi: int
    yazar_id: Optional[int] = Field(default=None, foreign_key="yazar.id")

    yazar: Optional["Yazar"] = Relationship(back_populates="kitaplar")
    odunc_kayitlari: List["OduncKayitlar"] = Relationship(back_populates="kitap")

class Uye(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ad: str
    soyad: str
    mail: str = Field(unique=True)

    odunc_kayitlari: List["OduncKayitlar"] = Relationship(back_populates="uye")

class OduncKayitlar(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kitap_id: Optional[int] = Field(default=None, foreign_key="kitap.id")
    uye_id: Optional[int] = Field(default=None, foreign_key="uye.id")
    alis_tarihi: date
    iade_tarihi: Optional[date] = None
    iade_edildi_mi: bool = Field(default=False)

    kitap: Optional["Kitap"] = Relationship(back_populates="odunc_kayitlari")
    uye: Optional["Uye"] = Relationship(back_populates="odunc_kayitlari")   