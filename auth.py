import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select

from database import get_session
from models import Yonetici, KayitIstek, GirisIstek

load_dotenv()

guvenlik_semasi = HTTPBearer()
GIZLI_ANAHTAR = os.getenv("GIZLI_ANAHTAR")
if not GIZLI_ANAHTAR:
    raise RuntimeError("GIZLI_ANAHTAR .env dosyasında tanımlı değil")
ALGORITMA = "HS256"
TOKEN_GECERLILIK_SURESI = 60

sifre_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def token_olustur(kullanici_adi: str):
    son_kullanma = datetime.utcnow() + timedelta(minutes=TOKEN_GECERLILIK_SURESI)
    veri = {
        "sub": kullanici_adi,
        "exp": son_kullanma
    }

    token = jwt.encode(veri, GIZLI_ANAHTAR, algorithm=ALGORITMA)

    return token

def token_dogrula(kimlik: HTTPAuthorizationCredentials = Depends(guvenlik_semasi)):
    
    token = kimlik.credentials

    try:
        veri = jwt.decode(token, GIZLI_ANAHTAR, algorithms=[ALGORITMA])
        kullanici_adi = veri.get("sub")
        if kullanici_adi is None:
            raise HTTPException(status_code=401, detail="Geçersiz token!")
        return kullanici_adi
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token!")

@router.post("/kayit")
def kayit_ol(istek: KayitIstek, session: Session = Depends(get_session)):
    sorgu = select(Yonetici).where(Yonetici.kullanici_adi == istek.kullanici_adi)
    mevcut = session.exec(sorgu).first()

    if mevcut:
        raise HTTPException(status_code=409, detail="Bu kullanıcı adı zaten alınmış")
    
    yeni_yonetici = Yonetici(
        kullanici_adi=istek.kullanici_adi,
        sifre_hash=sifre_context.hash(istek.sifre)
    )

    session.add(yeni_yonetici)
    session.commit()

    return {"mesaj": f"{istek.kullanici_adi} başarıyla kayıt oldu"}

@router.post("/giris")
def giris_yap(istek: GirisIstek, session: Session = Depends(get_session)):
    sorgu = select(Yonetici).where(Yonetici.kullanici_adi == istek.kullanici_adi)
    yonetici = session.exec(sorgu).first()

    if yonetici is None or not sifre_context.verify(istek.sifre, yonetici.sifre_hash):
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı!")

    access_token = token_olustur(yonetici.kullanici_adi)
    return {"access_token": access_token, "token_type": "bearer"}