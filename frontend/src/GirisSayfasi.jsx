import { useState } from 'react'

function App() {
  const [kullaniciAdi, setKullaniciAdi] = useState("")
  const [sifre, setSifre] = useState("")
  const [mesaj, setMesaj] = useState("")

  const girisYap = async () => {
    const cevap = await fetch("http://localhost:8000/giris", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        kullanici_adi: kullaniciAdi,
        sifre: sifre
      })
    })
    if (cevap.ok) {
      const veri = await cevap.json()
      setMesaj("Giriş Başarılı!")
    } else {
      setMesaj("Kullanıcı adı veya şifre hatalı!")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-80">
        <h1 className="text-2xl font-bold mb-8 text-gray-800">Giriş</h1>

        <input
          type="text"
          placeholder="Kullanıcı adı"
          value={kullaniciAdi}
          onChange={(e) => setKullaniciAdi(e.target.value)}
          className="w-full border border-gray-300 rounded p-2 mb-4"
          />
        
        <input
          type="password"
          placeholder="Şifre"
          value={sifre}
          onChange={(e) => setSifre(e.target.value)}
          className="w-full border border-gray-300 rounded p-2 mb-4"
          />
        
        <button
          onClick={girisYap}
          className="w-full bg-blue-600 text-white rounded p-2 font-semibold hover:bg-blue-700">
          Giris Yap
        </button>

        {mesaj && (
          <p className="mt-4 text-center text-sm text-gray-700">{mesaj}
          </p>
          )}

      </div>




    </div>
  )
}

export default App