import { useState } from 'react'
import GirisSayfasi from './GirisSayfasi'
import KayitSayfasi from './KayitSayfasi'
import Anasayfa from './Anasayfa'

function App() {
  const [token, setToken] = useState(null)
  const [sayfa, setSayfa] = useState("giris")

  const girisBasarili = (yeniToken) => {
    setToken(yeniToken)
  }

  if (token) {
    return <Anasayfa />
  }

  if (sayfa === "kayit") {
    return <KayitSayfasi girisSayfasinaGit={() => setSayfa("giris")} />

  }
  return (
    <GirisSayfasi
      onBasarili={girisBasarili}
      kayitSayfasinaGit={() => setSayfa("kayit")}
      />
   
  )
}

export default App