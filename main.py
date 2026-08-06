from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import veritabani_hazirla, get_session
from models import Yazar, Kitap, Uye, OduncKayitlar, YazarEkle, KitapEkle, UyeEkle, OduncKayitEkle, YazarGuncelle, KitapGuncelle, UyeGuncelle
from auth import router as auth_router, token_dogrula
from datetime import date

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
        raise HTTPException(status_code=409, detail="Bu kitaba ait ödünç kayıtları var, önce onları güncelleyin!")

    session.delete(kitap)
    session.commit()
    return {"mesaj": f"{kitap_id} numaralı kitap silindi"}

@app.get("/uyeler")
def uyeleri_listele(session: Session = Depends(get_session)):
    sorgu = select(Uye)
    uyeler = session.exec(sorgu).all()
    return uyeler

@app.get("/uyeler/{uye_id}")
def uye_bilgisi(uye_id: int, session: Session = Depends(get_session)):
    uye = session.get(Uye, uye_id)

    if uye is None:
        raise HTTPException(status_code=404, detail="Üye bulunamadı!")
    
    return uye

@app.post("/uyeler")
def uye_ekle(istek: UyeEkle, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    sorgu = select(Uye).where(Uye.mail == istek.mail)
    mevcut = session.exec(sorgu).first()

    if mevcut:
        raise HTTPException(status_code=409, detail="Bu mail adresi zaten kayıtlı!")

    yeni_uye = Uye(ad=istek.ad, soyad=istek.soyad, mail=istek.mail)
    session.add(yeni_uye)
    session.commit()
    session.refresh(yeni_uye)

    return {"mesaj": f"{yeni_uye.ad} {yeni_uye.soyad} sisteme eklendi", "uye": yeni_uye}

@app.delete("/uyeler/{uye_id}")
def uye_sil(uye_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    uye = session.get(Uye, uye_id)

    if uye is None:
        raise HTTPException(status_code=404, detail="Üye bulunamadı!")
    
    sorgu = select(OduncKayitlar).where(OduncKayitlar.uye_id == uye_id)
    bagli_kayit = session.exec(sorgu).first()

    if bagli_kayit:
        raise HTTPException(status_code=409, detail="Bu üyeye ait ödünç kayıtları var, önce onları güncelleyin!")

    session.delete(uye)
    session.commit()
    return {"mesaj": f"{uye_id} numaralı üye silindi"}

@app.get("/odunc-kayitlari")
def odunc_kayitlarini_listele(session: Session = Depends(get_session)):
    sorgu = select(OduncKayitlar)
    kayitlar = session.exec(sorgu).all()
    return kayitlar

@app.get("/odunc-kayitlari/{kayit_id}")
def odunc_kayit_bilgisi(kayit_id: int, session: Session = Depends(get_session)):
    kayit = session.get(OduncKayitlar, kayit_id)

    if kayit is None:
        raise HTTPException(status_code=404, detail="Ödünç kaydı bulunamadı!")

    return kayit

@app.post("/odunc-kayitlari")
def odunc_ver(istek: OduncKayitEkle, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    kitap = session.get(Kitap, istek.kitap_id)

    if kitap is None:
        raise HTTPException(status_code=404, detail=f"{istek.kitap_id} id'li kitap bulunamadı!")

    uye = session.get(Uye, istek.uye_id)

    if uye is None:
        raise HTTPException(status_code=404, detail=f"{istek.uye_id} id'li üye bulunamadı!")

    if kitap.stok_adedi <= 0:
        raise HTTPException(status_code=409, detail="Bu kitap şu an stokta yok!")

    yeni_kayit = OduncKayitlar(
        kitap_id = istek.kitap_id,
        uye_id = istek.uye_id,
        alis_tarihi = date.today(),
        iade_edildi_mi = False
    )

    kitap.stok_adedi -= 1

    session.add(yeni_kayit)
    session.commit()
    session.refresh(yeni_kayit)

    return {"mesaj": f"{kitap.baslik} kitabı {uye.ad} {uye.soyad} üyesine verildi", "kayit": yeni_kayit}


@app.put("/odunc-kayitlari/iade/{kayit_id}")
def iade_et(kayit_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    kayit = session.get(OduncKayitlar, kayit_id)

    if kayit is None:
        raise HTTPException(status_code=404, detail="Ödünç kaydı bulunamadı!")

    if kayit.iade_edildi_mi:
        raise HTTPException(status_code=409, detail="Bu kitap zaten iade edilmiş!")

    kitap = session.get(Kitap, kayit.kitap_id)

    kayit.iade_edildi_mi = True
    kayit.iade_tarihi = date.today()
    kitap.stok_adedi += 1

    session.commit()

    return {"mesaj": f"{kitap.baslik} kitabı iade edildi"}

@app.put("/yazarlar/guncelle/{yazar_id}")
def yazari_guncelle(istek: YazarGuncelle, yazar_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    yazar = session.get(Yazar, yazar_id)

    if yazar is None:
        raise HTTPException(status_code=404, detail=f"{yazar_id} id'li yazar bulunamadı!")

    yazar.ad = istek.ad
    yazar.soyad = istek.soyad

    session.commit()

    return {"mesaj": f"{yazar.id} id'li yazar güncellendi"}

@app.put("/kitaplar/guncelle/{kitap_id}")
def kitabi_guncelle(istek: KitapGuncelle, kitap_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    kitap = session.get(Kitap, kitap_id)

    if kitap is None:
        raise HTTPException(status_code=404, detail=f"{kitap_id} id'li kitap bulunamadı!")

    yazar = session.get(Yazar, istek.yazar_id)
    if yazar is None:
        raise HTTPException(status_code=404, detail=f"{istek.yazar_id} id'li yazar bulunamadı!")

    sorgu = select(OduncKayitlar).where(
        OduncKayitlar.kitap_id == kitap_id,
        OduncKayitlar.iade_edildi_mi == False)

    aktif_kayit = session.exec(sorgu).first()

    if aktif_kayit:
        raise HTTPException(status_code=409, detail="Bu kitabın kayıtlı ödünçleri var, önce onları güncelleyin!")

    kitap.baslik = istek.baslik
    kitap.stok_adedi = istek.stok_adedi
    kitap.yazar_id = istek.yazar_id

    session.commit()

    return {"mesaj": f"{kitap_id} id'li kitap güncellendi"}

@app.put("/uyeler/guncelle/{uye_id}")
def uye_guncelle(istek: UyeGuncelle, uye_id: int, kullanici_adi: str = Depends(token_dogrula), session: Session = Depends(get_session)):
    uye = session.get(Uye, uye_id)

    if uye is None:
        raise HTTPException(status_code=404, detail=f"{uye_id} id'li üye bulunamadı!")

    uye.ad = istek.ad
    uye.soyad = istek.soyad
    uye.mail = istek.mail

    session.commit()

    return {"mesaj": f"{uye_id} id'li üye güncellendi"}