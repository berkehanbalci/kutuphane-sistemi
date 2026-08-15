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

  const yazarlariGetir = async () => {
    const cevap = await fetch("http://localhost:8000/yazarlar")
    const veri = await cevap.json()
    setYazarlar(veri)
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

  useEffect(() => {
    yazarlariGetir()
    kitaplariGetir()
    uyeleriGetir()
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
      setseciliYazarId("")
      kitaplariGetir()
    }
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
          {yazarlar.length === 0 && (
            <p className="text-gray-500">Henüz Yazar Eklenmemiş</p>
          )}
          {yazarlar.map((yazar) => (
            <div key={yazar.id} className="border-b border-gray-200 py-2">
              {yazar.ad} {yazar.soyad}
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
          {kitaplar.map((kitap) => (
            <div key={kitap.id} className="border-b border-gray-200 py-2">
              <span className="font-semibold">{kitap.baslik}</span>
              <span className="text-gray-500"> — {kitap.yazar_adi}</span>
              <span className="text-sm text-gray-400"> (Stok: {kitap.stok_adedi})</span>
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
          {uyeler.map((uye) => (
            <div key={uye.id} className="border-b border-gray-200 py-2">
              <div>
                <span className="font-semibold">{uye.ad} {uye.soyad}</span>
                <span className="text-sm text-gray-400"> — {uye.mail}</span>
              </div>
              {uye.odunc_kitaplari.length > 0 && (
                <div className="ml-4 mt-1 text-sm text-gray-500">
                  {uye.odunc_kitaplari.map((kayit, index) => (
                    <div key={index}>
                      {kayit.kitap_baslik} {kayit.iade_edildi_mi ? "(İade edildi)" : "(Ödünçte)"}
                    </div>
                  ))}
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
