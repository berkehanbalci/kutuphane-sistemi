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
    
    


