import { createContext, useState, useEffect } from 'react'
import { refreshToken } from '../api/auth'

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'))
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'))

  useEffect(() => {
    const validateToken = async () => {
      if (refreshToken && !accessToken) {
        try {
          const response = await refreshToken(refreshToken)
          setAccessToken(response.data.access_token)
          localStorage.setItem('accessToken', response.data.access_token)
        } catch (error) {
          setUser(null)
          setAccessToken(null)
          setRefreshToken(null)
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
        }
      }
    }
    validateToken()
  }, [accessToken, refreshToken])

  const login = (userData, access, refresh) => {
    setUser(userData)
    setAccessToken(access)
    setRefreshToken(refresh)
    localStorage.setItem('accessToken', access)
    localStorage.setItem('refreshToken', refresh)
  }

  const logout = () => {
    setUser(null)
    setAccessToken(null)
    setRefreshToken(null)
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  }

  return (
    <AuthContext.Provider value={{ user, accessToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}