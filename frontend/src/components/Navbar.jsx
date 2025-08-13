import { NavLink } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import '../css/Navbar.css'

function Navbar() {
  const { user, logout } = useContext(AuthContext)

  return (
    <nav className="navbar">
      <NavLink to="/" className="navbar-title">Where The Hell Is My Money</NavLink>
      <div className="navbar-buttons">
        {user ? (
          <>
            <NavLink to="/dashboard" className="navbar-button">Dashboard</NavLink>
            <button onClick={logout} className="navbar-button">Logout</button>
          </>
        ) : (
          <>
            <NavLink to="/login" className="navbar-button">Login</NavLink>
            <NavLink to="/register" className="navbar-button">Register</NavLink>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar