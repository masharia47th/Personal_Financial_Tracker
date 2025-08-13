import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'
import { register } from '../api/auth'
import '../App.css'

function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [currency, setCurrency] = useState('USD')
  const [error, setError] = useState('')
  const { login: authLogin } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await register(username, password, currency)
      authLogin(response.data.user, null, null)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed')
    }
  }

  return (
    <div className="card">
      <h2>Register</h2>
      {error && <p className="error">{error}</p>}
      <div className="form-container">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="form-input"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="form-input"
        />
        <select
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          className="form-input"
        >
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="GBP">GBP</option>
          <option value="KES">KES</option>
        </select>
        <button onClick={handleSubmit} className="form-button">Register</button>
      </div>
    </div>
  )
}

export default Register