import { reactive } from 'vue'
import { navigateTo } from '../router.js'

export const authStore = reactive({
  token: localStorage.getItem('token') || null,
  currentUser: null,
  isAuthenticated: false
})

export async function initAuth() {
  if (authStore.token) {
    try {
      const res = await fetch('http://localhost:8000/api/me', {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (res.ok) {
        authStore.currentUser = await res.json()
        authStore.isAuthenticated = true
      } else {
        logout()
      }
    } catch (e) {
      logout()
    }
  }
}

export function setToken(token) {
  authStore.token = token
  localStorage.setItem('token', token)
}

export function logout() {
  authStore.token = null
  authStore.currentUser = null
  authStore.isAuthenticated = false
  localStorage.removeItem('token')
  navigateTo('/auth')
}

export function canAccessAdmin() {
  return authStore.currentUser?.role === 'admin' || authStore.currentUser?.role === 'super_admin'
}

