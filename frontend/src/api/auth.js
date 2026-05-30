import { request } from './request'

export const authApi = {
  login(username, password) {
    return request('/api/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
  },
  
  register(username, password) {
    return request('/api/register', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
  },
  
  getMe() {
    return request('/api/me')
  }
}
