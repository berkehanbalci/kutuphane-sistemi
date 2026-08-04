from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select

from database import veritabani_hazirla, get_session
from models import Yazar, Kitap, Uye, OduncKayitlar, YazarEkle
from auth import router as auth_router, token_dogrula

app = FastAPI()

veritabani_hazirla()

app.include_router(auth_router)

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Kütüphane Sistemi API Çalışıyor!"}

@app.get("/yazarlar")
def yazarlari_listele(session: Session = Depends(get_session)):
    sorgu = select(Yazar)
    yazarlar = session.exec(sorgu).all()
    return yazarlar

@app.get("/yazarlar/{yazar_id}")
def yazar_bilgisi(yazar_id: int, session: Session = Depends(get_session)):
    yazar = session.get(Yazar, yazar_id)
    if yazar is None:
        raise HTTPException(status_code=404, detail="Yazar bulunamadı!")
    return yazar

@app.post("/yazarlar")
def yazar_ekle(istek: YazarEkle, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    sorgu = select(Yazar).where(Yazar.ad == istek.ad, Yazar.soyad == istek.soyad)
    mevcut = session.exec(sorgu).first()
    if mevcut:
        raise HTTPException(status_code=409, detail="Bu yazar zaten kayıtlı!")

    yeni_yazar = Yazar(ad=istek.ad, soyad=istek.soyad)
    session.add(yeni_yazar)
    session.commit()
    session.refresh(yeni_yazar)
    return {"mesaj": f"{yeni_yazar.ad} {yeni_yazar.soyad} sisteme eklendi", "yazar": yeni_yazar}

@app.delete("/yazarlar/{yazar_id}")
def yazar_sil(yazar_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    yazar = session.get(Yazar, yazar_id)
    if yazar is None:
        raise HTTPException(status_code=404, detail="Yazar bulunamadı!")
    
    session.delete(yazar)
    session.commit()
    return {"mesaj": f"{yazar_id} numaralı yazar silindi"}


