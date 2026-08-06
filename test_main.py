def test_ana_sayfa(client):
    cevap = client.get("/")

    assert cevap.status_code == 200
    assert cevap.json() == {"mesaj": "Kütüphane Sistemi API Çalışıyor!"}

def test_bos_yazarlar_listesi(client):
    cevap = client.get("/yazarlar")

    assert cevap.status_code == 200
    assert cevap.json() == []

def test_yazar_ekle(client, token):
    cevap = client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    assert cevap.status_code == 200
    assert "eklendi" in cevap.json()["mesaj"]

def test_ayni_yazar_tekrar_eklenemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    cevap = client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    assert cevap.status_code == 409

def test_yazar_sil(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    cevap = client.delete("/yazarlar/1", headers=token)

    assert cevap.status_code == 200

    tekrar = client.delete("/yazarlar/1", headers=token)

    assert tekrar.status_code == 404

def test_yazarin_kitabi_varsa_silinemez(client, token):

    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    },
    headers=token)

    cevap = client.delete("/yazarlar/1", headers=token)

    assert cevap.status_code == 409

def test_yazar_guncelle(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    cevap = client.put("/yazarlar/guncelle/1", json={
        "ad": "Ali",
        "soyad": "Pamuk"
    },
    headers=token)

    assert cevap.status_code == 200

def test_yanlis_idli_yazar_guncellenemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    cevap = client.put("/yazarlar/guncelle/999", json={
        "ad": "Ali",
        "soyad": "Pamuk"
    },
    headers=token)

    assert cevap.status_code == 404

def test_kitap_ekle(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)
    
    cevap = client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    },
    headers=token)

    assert cevap.status_code == 200
    assert "eklendi" in cevap.json()["mesaj"]

def test_ayni_kitap_eklenemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    },
    headers=token)

    cevap = client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    },
    headers=token)

    assert cevap.status_code == 409

def test_geçersiz_idli_yazar_kitap_eklenemez(client, token):

    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    },
    headers=token)
    cevap = client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 2
    },
    headers=token)

    assert cevap.status_code == 404

def test_kitap_sil(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    cevap = client.delete("/kitaplar/1", headers=token)
    assert cevap.status_code == 200

    tekrar = client.delete("/kitaplar/1", headers=token)
    assert tekrar.status_code == 404


def test_odunctekiyken_kitap_silinemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    client.post("/uyeler", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "ahmet@ornek.com"
    }, headers=token)

    client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 1
    }, headers=token)

    cevap = client.delete("/kitaplar/1", headers=token)
    assert cevap.status_code == 409


def test_kitap_guncelle(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    cevap = client.put("/kitaplar/guncelle/1", json={
        "baslik": "Yeni Başlık",
        "stok_adedi": 10,
        "yazar_id": 1
    }, headers=token)

    assert cevap.status_code == 200


def test_yanlis_idli_kitap_guncellenemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    cevap = client.put("/kitaplar/guncelle/999", json={
        "baslik": "Yeni Başlık",
        "stok_adedi": 10,
        "yazar_id": 1
    }, headers=token)

    assert cevap.status_code == 404


def test_yanlis_yazarla_kitap_guncellenemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    cevap = client.put("/kitaplar/guncelle/1", json={
        "baslik": "Yeni Başlık",
        "stok_adedi": 10,
        "yazar_id": 999
    }, headers=token)

    assert cevap.status_code == 404


def test_odunctekiyken_kitap_guncellenemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    client.post("/uyeler", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "ahmet@ornek.com"
    }, headers=token)

    client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 1
    }, headers=token)

    cevap = client.put("/kitaplar/guncelle/1", json={
        "baslik": "Yeni Başlık",
        "stok_adedi": 10,
        "yazar_id": 1
    }, headers=token)

    assert cevap.status_code == 409

def test_uye_ekle(client, token):
    
    cevap = client.post("/uyeler", json={
        "ad": "Ali",
        "soyad": "Aslan",
        "mail": "test@gmail.com"
    },
    headers=token)

    assert cevap.status_code == 200
    assert "eklendi" in cevap.json()["mesaj"]

def test_kullanilan_mail_eklenemez(client, token):
    client.post("/uyeler", json={
        "ad": "Ali",
        "soyad": "Aslan",
        "mail": "test@gmail.com"
    },
    headers=token)

    cevap = client.post("/uyeler", json={
        "ad": "Ali",
        "soyad": "Aslan",
        "mail": "test@gmail.com"
    },
    headers=token)

    assert cevap.status_code == 409


def test_odunctekiyken_uye_silinemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    client.post("/uyeler", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "ahmet@ornek.com"
    }, headers=token)

    client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 1
    }, headers=token)

    cevap = client.delete("/uyeler/1", headers=token)
    assert cevap.status_code == 409


def test_uye_guncelle(client, token):
    client.post("/uyeler", json={
        "ad": "Ali",
        "soyad": "Aslan",
        "mail": "test@gmail.com"
    },
    headers=token)

    cevap = client.put("/uyeler/guncelle/1", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "test@gmail.com"
    },
    headers=token)

    assert cevap.status_code == 200


def test_yanlis_idli_uye_guncellenemez(client, token):
    client.post("/uyeler", json={
        "ad": "Ali",
        "soyad": "Aslan",
        "mail": "test@gmail.com"
    },
    headers=token)

    cevap = client.put("/uyeler/guncelle/999", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "test@gmail.com"
    },
    headers=token)
    assert cevap.status_code == 404
