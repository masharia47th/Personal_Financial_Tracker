import api from './index'

export const register = async (username, password, currency = 'USD') => {
  return api.post('/auth/register', { username, password, currency })
}

export const login = async (username, password) => {
  return api.post('/auth/login', { username, password })
}

export const refreshToken = async (refreshToken) => {
  return api.post('/auth/refresh', { refresh_token: refreshToken })
}