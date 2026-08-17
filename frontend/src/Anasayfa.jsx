import { useState, useEffect } from "react";

function Anasayfa({ token }) {
  const [yazarlar, setYazarlar] = useState([])
  const [yeniAd, setYeniAd] = useState("")
  const [yeniSoyad, setYeniSoyad] = useState("")
  const [kitaplar, setKitaplar] = useState([])
  const [yeniBaslik, setYeniBaslik] = useState("")
  const [yeniStok, setYeniStok] = useState("")
  const [seciliYazarId, setSeciliYazarId] = useState("")
  const [uyeler, setUyeler] = useState([])
  const [yeniUyeAd, setYeniUyeAd] = useState("")
  const [yeniUyeSoyad, setYeniUyeSoyad] = useState("")
  const [yeniUyeMail, setYeniUyeMail] = useState("")
  const [oduncKayitlari, setOduncKayitlari] = useState([])
  const [seciliKitapId, setSeciliKitapId] = useState("")
  const [seciliUyeId, setSeciliUyeId] = useState("")
  const [duzenlenenYazarId, setDuzenlenenYazarId] = useState(null)
  const [duzenAd, setDuzenAd] = useState("")
  const [duzenSoyad, setDuzenSoyad] = useState("")
  const [duzenlenenKitapId, setDuzenlenenKitapId] = useState(null)
  const [duzenBaslik, setDuzenBaslik] = useState("")
  const [duzenStok, setDuzenStok] = useState("")
  const [duzenYazarId, setDuzenYazarId] = useState("")
  const [duzenlenenUyeId, setDuzenlenenUyeId] = useState(null)
  const [duzenUyeAd, setDuzenUyeAd] = useState("")
  const [duzenUyeSoyad, setDuzenUyeSoyad] = useState("")
  const [duzenUyeMail, setDuzenUyeMail] = useState("")


  const yazarlariGetir = async () => {
    const cevap = await fetch("http://localhost:8000/yazarlar")
    if (cevap.ok) {
      const veri = await cevap.json()
      setYazarlar(veri)
    }
  }

  const kitaplariGetir = async () => {
    const cevap = await fetch("http://localhost:8000/kitaplar")
    const veri = await cevap.json()
    setKitaplar(veri)
  }

  const uyeleriGetir = async () => {
    const cevap = await fetch("http://localhost:8000/uyeler")
    const veri = await cevap.json()
    setUyeler(veri)
  }

  const oduncKayitlariGetir = async () => {
    const cevap = await fetch("http://localhost:8000/odunc-kayitlari")
    const veri  = await cevap.json()
    setOduncKayitlari(veri)
  }

  useEffect(() => {
    yazarlariGetir()
    kitaplariGetir()
    uyeleriGetir()
    oduncKayitlariGetir()
  }, [])

  const yazarEkle = async () => {
    const cevap = await fetch("http://localhost:8000/yazarlar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ ad: yeniAd, soyad: yeniSoyad })
    })
    if (cevap.ok) {
      setYeniAd("")
      setYeniSoyad("")
      yazarlariGetir()
    }
  }

  const uyeEkle = async () => {
    const cevap = await fetch("http://localhost:8000/uyeler", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ ad: yeniUyeAd, soyad: yeniUyeSoyad, mail: yeniUyeMail})
    })
    if (cevap.ok) {
      setYeniUyeAd("")
      setYeniUyeSoyad("")
      setYeniUyeMail("")
      uyeleriGetir()
    }
  }
  
  const kitapEkle = async () => {
    if (!yeniBaslik || !yeniStok || !seciliYazarId) {
      return alert("Lütfen tüm alanları doldurun ve bir yazar seçin.")
    }
    const cevap = await fetch("http://localhost:8000/kitaplar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        baslik: yeniBaslik,
        stok_adedi: parseInt(yeniStok),
        yazar_id: parseInt(seciliYazarId)
      })
    })
    if (cevap.ok) {
      setYeniBaslik("")
      setYeniStok("")
      setSeciliYazarId("")
      kitaplariGetir()
    }
  }

  const oduncVer = async () => {
    const cevap = await fetch("http://localhost:8000/odunc-kayitlari", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        kitap_id: parseInt(seciliKitapId),
        uye_id: parseInt(seciliUyeId)
      })
    })
    if (cevap.ok) {
      setSeciliKitapId("")
      setSeciliUyeId("")
      oduncKayitlariGetir()
      kitaplariGetir()
      uyeleriGetir()
    }
  }
  const iadeEt = async (kayitId) => {
    const cevap = await fetch(`http://localhost:8000/odunc-kayitlari/iade/${kayitId}`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    if (cevap.ok) {
      oduncKayitlariGetir()
      kitaplariGetir()
      uyeleriGetir()
    }
  }

  const yazarSil = async (yazarId) => {
    const onay = window.confirm("Bu yazarı silmek istediğinize emin misiniz?")
    if (!onay) return

    const cevap = await fetch(`http://localhost:8000/yazarlar/${yazarId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    })
    if (cevap.ok) {
      yazarlariGetir()
    } else {
      const hata = await cevap.json()
      alert(hata.detail)
    }
  }
  const kitapSil = async (kitapId) => {
    const onay = window.confirm("Bu kitabı silmek istediğinize emin misiniz?")
    if (!onay) return

    const cevap = await fetch(`http://localhost:8000/kitaplar/${kitapId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    })
    if (cevap.ok) {
      kitaplariGetir()
    } else {
      const hata = await cevap.json()
      alert(hata.detail)
    }
  }
  const uyeSil = async (uyeId) => {
    const onay = window.confirm("Bu üyeyi silmek istediğinize emin misiniz?")
    if (!onay) return

    const cevap = await fetch(`http://localhost:8000/uyeler/${uyeId}`, {
      method: "DELETE",
      headers: { "Authorization": `Bearer ${token}` }
    })
    if (cevap.ok) {
      uyeleriGetir()
    } else {
      const hata = await cevap.json()
      alert(hata.detail)
    }
  }

  const yazarGuncelle = async () => {
    const cevap = await fetch(`http://localhost:8000/yazarlar/guncelle/${duzenlenenYazarId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ ad: duzenAd, soyad: duzenSoyad })
    })
    if (cevap.ok) {
      setDuzenlenenYazarId(null)
      yazarlariGetir()
    } else {
      const hata = await cevap.json()
      alert(hata.detail)
    }
  }

  const kitapGuncelle = async () => {
    const cevap = await fetch(`http://localhost:8000/kitaplar/guncelle/${duzenlenenKitapId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ baslik: duzenBaslik, stok_adedi: duzenStok, yazar_id: duzenYazarId })
    })
    if (cevap.ok) {
      setDuzenlenenKitapId(null)
      kitaplariGetir()
    } else {
      const hata = await cevap.json()
      alert(hata.detail)
    }
  }

  const uyeGuncelle = async () => {
    const cevap = await fetch(`http://localhost:8000/uyeler/guncelle/${duzenlenenUyeId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        ad: duzenUyeAd,
        soyad: duzenUyeSoyad,
        mail: duzenUyeMail
      })
    })
    if (cevap.ok) {
      setDuzenlenenUyeId(null)
      uyeleriGetir()
    } else {
      const hata = await cevap.json()
      alert(hata.detail)
    }
  }

  const duzenlemeyeBasla = (yazar) => {
    setDuzenlenenYazarId(yazar.id)
    setDuzenAd(yazar.ad)
    setDuzenSoyad(yazar.soyad)
  }

  const kitapDuzenlemeyeBasla = (kitap) => {
    setDuzenlenenKitapId(kitap.id)
    setDuzenBaslik(kitap.baslik)
    setDuzenStok(kitap.stok_adedi)
    setDuzenYazarId(kitap.yazar_id)
  }

  const uyeDuzenlemeyeBasla = (uye) => {
    setDuzenlenenUyeId(uye.id)
    setDuzenUyeAd(uye.ad)
    setDuzenUyeSoyad(uye.soyad)
    setDuzenUyeMail(uye.mail)
  }
  

  const duzenlemeyiIptalEt = () => {
    setDuzenlenenYazarId(null)
  }

  const kitapDuzenlemeyiIptalEt = () => {
    setDuzenlenenKitapId(null)
  }

  const uyeDuzenlemeyiIptalEt = () => {
    setDuzenlenenUyeId(null)
  }
  

 return (
  <div className="min-h-screen bg-gray-100 p-8">
    <h1 className="text-3xl font-bold text-gray-800 mb-6">Kütüphane Sistemi</h1>

    <div className="grid grid-cols-3 gap-6">

      <div>
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Yeni Yazar Ekle</h2>
          <input
            type="text"
            placeholder="Ad"
            value={yeniAd}
            onChange={(e) => setYeniAd(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <input
            type="text"
            placeholder="Soyad"
            value={yeniSoyad}
            onChange={(e) => setYeniSoyad(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <button
            onClick={yazarEkle}
            className="w-full bg-blue-600 text-white rounded p-2 font-semibold hover:bg-blue-700"
          >
            Yazar Ekle
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Yazarlar</h2>
          {yazarlar?.length === 0 && (
            <p className="text-gray-500">Henüz Yazar Eklenmemiş</p>
          )}
          {yazarlar?.map((yazar) => (
            <div key ={yazar.id}
              className="border-b border-gray-200 py-2">
              {duzenlenenYazarId === yazar.id ? (
                <div>
                  <input
                    type="text"
                    value={duzenAd}
                    onChange={(e) => setDuzenAd(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                    />
                  
                  <input
                    type="text"
                    value={duzenSoyad}
                    onChange={(e) => setDuzenSoyad(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                    />
                  <div className="flex gap-2">
                    <button
                      onClick={yazarGuncelle}
                      className="text-xs text-green-600 hover:underline">
                        Kaydet
                    </button>

                    <button
                      onClick={duzenlemeyiIptalEt} 
                      className="text-xs text-gray-500 hover:underline">
                        İptal
                    </button>
                  </div>
                </div>
                
              ) : (
                <div className="flex justify-between items-center">
                  <span>{yazar.ad} {yazar.soyad}</span>
                  <div className="flex gap-2">
                    <button 
                      onClick={() => duzenlemeyeBasla(yazar)}
                      className="text-xs text-blue-600 hover:underline">
                        Düzenle
                    </button>
                    <button
                      onClick={() => yazarSil(yazar.id)}
                      className="text-xs text-red-600 hover:underline">
                        Sil
                    </button>
                    
                  </div>
                </div>

              )}
            </div>
          ))}
         
        </div>
        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Ödünç Ver</h2>

          <select
            value={seciliKitapId}
            onChange={(e) => setSeciliKitapId(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          >
            <option value="">Kitap Seçin</option>
            {kitaplar?.map((kitap) => (
              <option key={kitap.id} value={kitap.id}>
                {kitap.baslik}
              </option>
            ))}
          </select>

          <select
            value={seciliUyeId}
            onChange={(e) => setSeciliUyeId(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          >
            <option value="">Üye Seçin</option>
            {uyeler?.map((uye) => (
              <option key={uye.id} value={uye.id}>
                {uye.ad} {uye.soyad}
              </option>
            ))}
          </select>
          <button
            onClick={oduncVer}
            className="w-full bg-blue-600 text-white rounded p-2 font-semibold hover:bg-blue-700"
            >
              Ödünç Ver
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mt-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Ödünç Kayıtları</h2>
          {oduncKayitlari?.length === 0 && (
            <p className="text-gray-500">Henüz Ödünç Kaydı Yok</p>
          )}
          {oduncKayitlari?.filter((kayit) => !kayit.iade_edildi_mi).map((kayit) => (
            <div key={kayit.id} className="border-b border-gray-200 py-2">
              <div className="text-sm">
                <span className="font-semibold">{kayit.kitap_baslik}</span>
                <span className="text-gray-500"> — {kayit.uye_adi}</span> 
              </div>
              {kayit.iade_edildi_mi ? (
                <span className="text-xs text-green-600">İade Edildi</span>
              ) : (
                <button
                onClick={() => iadeEt(kayit.id)}
                className="text-xs text-blue-600 hover:underline"
                >
                  İade Et
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
      

      <div>
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Yeni Kitap Ekle</h2>

          <input
            type="text"
            placeholder="Başlık"
            value={yeniBaslik}
            onChange={(e) => setYeniBaslik(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <input
            type="number"
            placeholder="Stok Adedi"
            value={yeniStok}
            onChange={(e) => setYeniStok(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <select
            value={seciliYazarId}
            onChange={(e) => setSeciliYazarId(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          >
            <option value="">Yazar seçin</option>
            {yazarlar.map((yazar) => (
              <option key={yazar.id} value={yazar.id}>
                {yazar.ad} {yazar.soyad}
              </option>
            ))}
          </select>

          <button
            onClick={kitapEkle}
            className="w-full bg-blue-600 text-white rounded p-2 font-semibold hover:bg-blue-700"
          >
            Kitap Ekle
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Kitaplar</h2>
          {kitaplar.length === 0 && (
            <p className="text-gray-500">Henüz Kitap Eklenmemiş</p>
          )}
          {kitaplar?.map((kitap) => (
            <div key={kitap.id} className="border-b border-gray-200 py-2">
              {duzenlenenKitapId === kitap.id ? (
                <div>
                  <input
                    type="text"
                    value={duzenBaslik}
                    onChange={(e) => setDuzenBaslik(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                  />

                  <input
                    type="number"
                    value={duzenStok}
                    onChange={(e) => setDuzenStok(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                  />

                  <select
                    value={duzenYazarId}
                    onChange={(e) => setDuzenYazarId(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                  >
                    <option value=""Yazar seçin></option>
                    {yazarlar?.map((yazar) => (
                      <option key={yazar.id} value={yazar.id}>
                        {yazar.ad} {yazar.soyad}
                      </option>
                    ))}
                  </select>
                  <div className="flex gap-2">
                    <button
                      onClick={kitapGuncelle}
                      className="text-xs text-green-600 hover:underline">
                        Kaydet
                    </button>
                    <button
                      onClick={kitapDuzenlemeyiIptalEt}
                      className="text-xs text-gray-500 hover:underline">
                        İptal
                    </button>
                  </div>
                </div>
              ) : (
                <div className="flex justify-between items-center">
                  <div>
                    <span className="font-semibold">{kitap.baslik}</span>
                    <span className="text-gray-500"> — {kitap.yazar_id}</span>
                    <span className="text-sm text-gray-400"> (Stok: {kitap.stok_adedi})</span>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => kitapDuzenlemeyeBasla(kitap)}
                      className="text-xs text-blue-600 hover:underline">
                        Düzenle
                    </button>
                    <button
                      onClick={() => kitapSil(kitap.id)}
                      className="text-xs text-red-600 hover:underline">
                        Sil
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div>
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Yeni Üye Ekle</h2>

          <input
            type="text"
            placeholder="Ad"
            value={yeniUyeAd}
            onChange={(e) => setYeniUyeAd(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <input
            type="text"
            placeholder="Soyad"
            value={yeniUyeSoyad}
            onChange={(e) => setYeniUyeSoyad(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <input
            type="email"
            placeholder="E-posta"
            value={yeniUyeMail}
            onChange={(e) => setYeniUyeMail(e.target.value)}
            className="w-full border border-gray-300 rounded p-2 mb-3"
          />

          <button
            onClick={uyeEkle}
            className="w-full bg-blue-600 text-white rounded p-2 font-semibold hover:bg-blue-700"
          >
            Üye Ekle
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-800">Üyeler</h2>
          {uyeler.length === 0 && (
            <p className="text-gray-500">Henüz Üye Eklenmemiş</p>
          )}
          {uyeler?.map((uye) => (
            <div key={uye.id} className="border-b border-gray-200 py-2">
              {duzenlenenUyeId === uye.id ? (
                <div>
                  <input
                    type="text"
                    value={duzenUyeAd}
                    onChange={(e) => setDuzenUyeAd(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                  />
                  <input
                    type="text"
                    value={duzenUyeSoyad}
                    onChange={(e) => setDuzenUyeSoyad(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                  />
                  <input
                    type="email"
                    value={duzenUyeMail}
                    onChange={(e) => setDuzenUyeMail(e.target.value)}
                    className="w-full border border-gray-300 rounded p-1 mb-1 text-sm"
                  />
                  <div className="flex gap-2">
                    <button 
                      onClick={uyeGuncelle} 
                      className="text-xs text-green-600 hover:underline">
                      Kaydet
                    </button>
                    <button 
                      onClick={uyeDuzenlemeyiIptalEt} 
                      className="text-xs text-gray-500 hover:underline">
                      İptal
                    </button>
                  </div>
                </div>
              ) : (
                <div>
                  <div className="flex justify-between items-center">
                    <div>
                      <span className="font-semibold">{uye.ad} {uye.soyad}</span>
                      <span className="text-sm text-gray-400"> — {uye.mail}</span>
                    </div>
                    <div className="flex gap-2">
                      <button onClick={() => uyeDuzenlemeyeBasla(uye)} className="text-xs text-blue-600 hover:underline">
                        Düzenle
                      </button>
                      <button onClick={() => uyeSil(uye.id)} className="text-xs text-red-600 hover:underline">
                        Sil
                      </button>
                    </div>
                  </div>
                  {uye.odunc_kitaplari?.length > 0 && (
                    <div className="ml-4 mt-1 text-sm text-gray-500">
                      {uye.odunc_kitaplari.map((kayit, index) => (
                        <div key={index}>
                          {kayit.kitap_baslik} {kayit.iade_edildi_mi ? "(İade edildi)" : "(Ödünçte)"}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

    </div>
  </div>
  )
}
export default Anasayfa
