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

def test_bos_odunc_listesi(client):
    cevap = client.get("/odunc-kayitlari")

    assert cevap.status_code == 200
    assert cevap.json() == []


def test_odunc_ver(client, token):
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

    cevap = client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 1
    }, headers=token)

    assert cevap.status_code == 200
    assert "verildi" in cevap.json()["mesaj"]


def test_odunc_verilince_stok_azalir(client, token):
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

    kitap = client.get("/kitaplar/1").json()
    assert kitap["stok_adedi"] == 4


def test_gecersiz_kitapla_odunc_verilemez(client, token):
    client.post("/uyeler", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "ahmet@ornek.com"
    }, headers=token)

    cevap = client.post("/odunc-kayitlari", json={
        "kitap_id": 999,
        "uye_id": 1
    }, headers=token)

    assert cevap.status_code == 404


def test_gecersiz_uyeyle_odunc_verilemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 5,
        "yazar_id": 1
    }, headers=token)

    cevap = client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 999
    }, headers=token)

    assert cevap.status_code == 404


def test_stokta_olmayan_kitap_odunc_verilemez(client, token):
    client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    client.post("/kitaplar", json={
        "baslik": "Test",
        "stok_adedi": 1,
        "yazar_id": 1
    }, headers=token)

    client.post("/uyeler", json={
        "ad": "Ahmet",
        "soyad": "Yılmaz",
        "mail": "ahmet@ornek.com"
    }, headers=token)

    client.post("/uyeler", json={
        "ad": "Mehmet",
        "soyad": "Demir",
        "mail": "mehmet@ornek.com"
    }, headers=token)

    client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 1
    }, headers=token)

    cevap = client.post("/odunc-kayitlari", json={
        "kitap_id": 1,
        "uye_id": 2
    }, headers=token)

    assert cevap.status_code == 409


def test_iade_et(client, token):
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

    cevap = client.put("/odunc-kayitlari/iade/1", headers=token)

    assert cevap.status_code == 200
    assert "iade edildi" in cevap.json()["mesaj"]


def test_iade_edilince_stok_artar(client, token):
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

    client.put("/odunc-kayitlari/iade/1", headers=token)

    kitap = client.get("/kitaplar/1").json()
    assert kitap["stok_adedi"] == 5


def test_tekrar_iade_edilemez(client, token):
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

    client.put("/odunc-kayitlari/iade/1", headers=token)

    cevap = client.put("/odunc-kayitlari/iade/1", headers=token)

    assert cevap.status_code == 409


def test_gecersiz_kayitla_iade_edilemez(client, token):
    cevap = client.put("/odunc-kayitlari/iade/999", headers=token)

    assert cevap.status_code == 404


def test_gecersiz_idli_odunc_kaydi_bulunamaz(client):
    cevap = client.get("/odunc-kayitlari/999")

    assert cevap.status_code == 404

def test_kayit_basarili(client):
    cevap = client.post("/kayit", json={
        "kullanici_adi": "yeni_kullanici",
        "sifre": "sifre123"
    })

    assert cevap.status_code == 200


def test_ayni_kullanici_iki_kez_kayit_olamaz(client):
    client.post("/kayit", json={
        "kullanici_adi": "admin",
        "sifre": "sifre123"
    })

    cevap = client.post("/kayit", json={
        "kullanici_adi": "admin",
        "sifre": "baska_sifre"
    })

    assert cevap.status_code == 409


def test_giris_basarili_token_donuyor(client):
    client.post("/kayit", json={
        "kullanici_adi": "admin",
        "sifre": "sifre123"
    })

    cevap = client.post("/giris", json={
        "kullanici_adi": "admin",
        "sifre": "sifre123"
    })

    assert cevap.status_code == 200
    assert "access_token" in cevap.json()


def test_yanlis_sifre_ile_giris_reddedilir(client):
    client.post("/kayit", json={
        "kullanici_adi": "admin",
        "sifre": "dogru_sifre"
    })

    cevap = client.post("/giris", json={
        "kullanici_adi": "admin",
        "sifre": "yanlis_sifre"
    })

    assert cevap.status_code == 401


def test_olmayan_kullanici_giris_yapamaz(client):
    cevap = client.post("/giris", json={
        "kullanici_adi": "hayalet",
        "sifre": "birsey"
    })

    assert cevap.status_code == 401


def test_tokensiz_korumali_endpoint_reddedilir(client):
    cevap = client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    })

    assert cevap.status_code in (401, 403)


def test_yanlis_token_ile_reddedilir(client):
    sahte_header = {"Authorization": "Bearer sahte_token_123"}

    cevap = client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=sahte_header)

    assert cevap.status_code == 401


def test_gecerli_token_ile_erisim_saglanir(client, token):
    cevap = client.post("/yazarlar", json={
        "ad": "Orhan",
        "soyad": "Pamuk"
    }, headers=token)

    assert cevap.status_code == 200