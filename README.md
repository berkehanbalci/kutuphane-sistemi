# 📚 Kütüphane Sistemi

[![Testler](https://github.com/berkehanbalci/kutuphane-sistemi/actions/workflows/test.yml/badge.svg)](https://github.com/berkehanbalci/kutuphane-sistemi/actions/workflows/test.yml)

Yazar, kitap, üye ve ödünç kayıtlarını yöneten, JWT tabanlı kimlik doğrulamalı, tam CRUD işlevselliğine sahip bir kütüphane yönetim sistemi. FastAPI + SQLModel backend, React + Tailwind frontend, Docker ile konteynerleştirilmiş, GitHub Actions ile otomatik test edilen bir full-stack proje.

## Özellikler

- 🔐 JWT tabanlı kullanıcı kaydı ve girişi
- 📖 Yazar, Kitap, Üye için tam CRUD (ekleme, listeleme, güncelleme, silme)
- 🔄 Ödünç verme / iade etme, otomatik stok yönetimi
- 🔗 SQLModel `Relationship` ile ilişkisel veri sorgulama (yazar adı, ödünç geçmişi vb.)
- ✅ 41 otomatik test (pytest), her push'ta GitHub Actions ile çalışıyor
- 🐳 Docker Compose ile tek komutla ayağa kalkan backend + frontend + veritabanı
- 🎨 React + Tailwind CSS ile duyarlı (responsive) arayüz

## Teknoloji Yığını

**Backend:** Python, FastAPI, SQLModel, PostgreSQL, JWT (python-jose), bcrypt (passlib)
**Frontend:** React, Vite, Tailwind CSS
**Test:** pytest
**DevOps:** Docker, Docker Compose, GitHub Actions (CI)

## Proje Yapısı

```
kutuphane_sistemi/
├── backend/
│   ├── app/                 # Uygulama kodu
│   │   ├── main.py          # API endpoint'leri
│   │   ├── models.py        # SQLModel veri modelleri
│   │   ├── database.py      # Veritabanı bağlantısı
│   │   └── auth.py          # Kimlik doğrulama (JWT)
│   ├── tests/                # pytest testleri
│   │   ├── conftest.py
│   │   └── test_main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/                  # React bileşenleri
│   │   ├── App.jsx
│   │   ├── GirisSayfasi.jsx
│   │   ├── KayitSayfasi.jsx
│   │   └── Anasayfa.jsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── .github/workflows/test.yml   # CI/CD
```

## Kurulum

### Seçenek 1 — Docker ile (önerilen)

```bash
git clone https://github.com/berkehanbalci/kutuphane-sistemi.git
cd kutuphane-sistemi
cp .env.example .env
```

`.env` dosyasını açıp `DB_PASSWORD` ve `GIZLI_ANAHTAR` değerlerini kendine göre doldur, sonra:

```bash
docker compose up --build
```

- Backend: `http://localhost:8000/docs`
- Frontend: `http://localhost:3000`

### Seçenek 2 — Yerel kurulum

**Backend:**
```bash
cd backend
pip install -r requirements.txt --break-system-packages
cp .env.example .env   # değerleri doldur
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Ortam Değişkenleri

| Değişken | Açıklama |
|---|---|
| `DB_HOST` | Veritabanı sunucu adresi |
| `DB_PORT` | Veritabanı portu |
| `DB_NAME` | Veritabanı adı |
| `DB_USER` | Veritabanı kullanıcı adı |
| `DB_PASSWORD` | Veritabanı şifresi |
| `GIZLI_ANAHTAR` | JWT token imzalama anahtarı |

## API Endpoint'leri

| Metot | Yol | Açıklama | Yetki |
|---|---|---|---|
| POST | `/kayit` | Kullanıcı kaydı | - |
| POST | `/giris` | Giriş, JWT token döner | - |
| GET | `/yazarlar` | Yazarları listele | - |
| GET | `/yazarlar/{id}` | Tek yazar getir | - |
| POST | `/yazarlar` | Yazar ekle | 🔒 |
| PUT | `/yazarlar/guncelle/{id}` | Yazar güncelle | 🔒 |
| DELETE | `/yazarlar/{id}` | Yazar sil | 🔒 |
| GET | `/kitaplar` | Kitapları listele (yazar adı dahil) | - |
| GET | `/kitaplar/{id}` | Tek kitap getir | - |
| POST | `/kitaplar` | Kitap ekle | 🔒 |
| PUT | `/kitaplar/guncelle/{id}` | Kitap güncelle | 🔒 |
| DELETE | `/kitaplar/{id}` | Kitap sil | 🔒 |
| GET | `/uyeler` | Üyeleri listele (ödünç geçmişi dahil) | - |
| POST | `/uyeler` | Üye ekle | 🔒 |
| PUT | `/uyeler/guncelle/{id}` | Üye güncelle | 🔒 |
| DELETE | `/uyeler/{id}` | Üye sil | 🔒 |
| GET | `/odunc-kayitlari` | Ödünç kayıtlarını listele | - |
| GET | `/odunc-kayitlari/{id}` | Tek ödünç kaydı getir | - |
| POST | `/odunc-kayitlari` | Kitap ödünç ver | 🔒 |
| PUT | `/odunc-kayitlari/iade/{id}` | Kitabı iade et | 🔒 |

🔒 = Kimlik doğrulama gerekli (`Authorization: Bearer <token>`)

Tüm endpoint'lerin detaylı, denenebilir dokümantasyonu için: `http://localhost:8000/docs`

## İş Kuralları

- Aynı ad-soyada sahip yazar tekrar eklenemez
- Aynı başlıklı kitap tekrar eklenemez
- Aynı mail adresine sahip üye tekrar eklenemez
- Stokta olmayan kitap ödünç verilemez
- Aynı üye, aynı kitabı iade etmeden ikinci kez alamaz
- Ödünçteki bir kitap güncellenemez veya silinemez
- Bağlı kitabı olan yazar silinemez
- Aktif ödünç kaydı olan üye silinemez

## Testleri Çalıştırma

```bash
cd backend
python -m pytest tests/ -v
```

41 test; auth, CRUD işlemleri, foreign key kontrolleri, stok yönetimi ve iş kurallarını kapsıyor. Her `push`'ta GitHub Actions üzerinde otomatik çalışıyor.

## Geliştirici

**Berkehan Balcı** — [GitHub](https://github.com/berkehanbalci)