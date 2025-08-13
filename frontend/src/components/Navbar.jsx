import { Link } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import '../css/Navbar.css'

function Navbar() {
  const { user, logout } = useContext(AuthContext)

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-title">Where The Hell Is My Money</Link>
      <div className="navbar-buttons">
        {user ? (
          <>
            <Link to="/dashboard" className="navbar-button">Dashboard</Link>
            <button onClick={logout} className="navbar-button">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="navbar-button">Login</Link>
            <Link to="/register" className="navbar-button">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar