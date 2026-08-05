from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import veritabani_hazirla, get_session
from models import Yazar, Kitap, Uye, OduncKayitlar, YazarEkle, KitapEkle
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

    sorgu = select(Kitap).where(Kitap.yazar_id == yazar_id)
    mevcut = session.exec(sorgu).first()

    if mevcut is not None:
        raise HTTPException(status_code=409, detail="Bu yazarın kayıtlı kitapları var, önce kitabı güncelleyin veya silin!")
    
    session.delete(yazar)
    session.commit()
    return {"mesaj": f"{yazar_id} numaralı yazar silindi"}

@app.get("/kitaplar")
def kitaplari_listele(session: Session = Depends(get_session)):
    sorgu = select(Kitap)
    kitaplar = session.exec(sorgu).all()
    return kitaplar

@app.get("/kitaplar/{kitap_id}")
def kitap_bilgisi(kitap_id: int, session: Session = Depends(get_session)):
    kitap = session.get(Kitap, kitap_id)

    if kitap is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı!")
    return kitap

@app.post("/kitaplar")
def kitap_ekle(istek: KitapEkle, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    yazar = session.get(Yazar, istek.yazar_id)
    
    if yazar is None:
        raise HTTPException(status_code=404, detail=f"{istek.yazar_id} id'li yazar bulunamadı!")
    
    sorgu = select(Kitap).where(Kitap.baslik == istek.baslik)
    mevcut = session.exec(sorgu).first()

    if mevcut:
        raise HTTPException(status_code=409, detail="Bu kitap zaten kayıtlı!")

    yeni_kitap = Kitap(baslik=istek.baslik, stok_adedi=istek.stok_adedi, yazar_id=istek.yazar_id)
    session.add(yeni_kitap)
    session.commit()
    session.refresh(yeni_kitap)

    return {"mesaj": f"{yeni_kitap.baslik} sisteme eklendi", "kitap": yeni_kitap}

@app.delete("/kitaplar/{kitap_id}")
def kitap_sil(kitap_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    kitap = session.get(Kitap, kitap_id)

    if kitap is None:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı!")
    
    sorgu = select(OduncKayitlar).where(OduncKayitlar.kitap_id == kitap_id)
    bagli_kayit = session.exec(sorgu).first()
    if bagli_kayit:
        raise HTTPException(status_code=409, detail="Bu kitaba ait ödünç kayıtları var, önce onları silin!")

    session.delete(kitap)
    session.commit()
    return {"mesaj": f"{kitap_id} numaralı kitap silindi"}