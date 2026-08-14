import { useState, useEffect } from "react";

function Anasayfa({ token }) {
  const [yazarlar, setYazarlar] = useState([])
  const [yeniAd, setYeniAd] = useState("")
  const [yeniSoyad, setYeniSoyad] = useState("")

  const yazarlariGetir = async () => {
    const cevap = await fetch("http://localhost:8000/yazarlar")
    const veri = await cevap.json()
    setYazarlar(veri)
  }

  useEffect(() => {
    yazarlariGetir()
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

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Kütüphane Sistemi</h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6 max-w-md">
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
          className="w-full bg-blue-600 text-white rounded p-2 font-semibold hover:bg-blue-600">
            Yazar Ekle
          </button>
      </div>
      <div className="bg-white rounded-lg shadow-md p-6 mb-6 max-w-md">
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
  )
}

export default Anasayfa
