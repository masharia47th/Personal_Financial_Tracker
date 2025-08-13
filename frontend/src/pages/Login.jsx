import { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'
import { login } from '../api/auth'
import '../App.css'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const { login: authLogin } = useContext(AuthContext)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const response = await login(username, password)
      authLogin(response.data.user, response.data.access_token, response.data.refresh_token)
      navigate('/')
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed')
    }
  }

  return (
    <div className="card">
      <h2>Login</h2>
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
        <button onClick={handleSubmit} className="form-button">Login</button>
      </div>
    </div>
  )
}

export default Login