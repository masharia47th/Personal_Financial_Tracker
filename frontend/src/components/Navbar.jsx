import { Link } from 'react-router-dom'
import '../css/Navbar.css'

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-title">Where The Hell Is My Money</Link>
      <div className="navbar-buttons">
        <Link to="/login" className="navbar-button">Login</Link>
        <Link to="/register" className="navbar-button">Register</Link>
      </div>
    </nav>
  )
}

export default Navbar