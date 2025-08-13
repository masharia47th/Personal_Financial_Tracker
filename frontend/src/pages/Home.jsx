import { useState } from 'react'
import reactLogo from '../assets/react.svg'
import Logo from '/logo.png'
import '../App.css'

function Home() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="/" target="_blank">
          <img src={Logo} className="logo" alt="Vite logo" />
        </a>
      </div>
      <h1>Where The Hell Is My Money</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          Fidget No: {count}
        </button>
      </div>
    </>
  )
}

export default Home