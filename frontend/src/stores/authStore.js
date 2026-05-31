import { defineStore } from 'pinia'
import { navigateTo } from '../router.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    currentUser: null,
    isAuthenticated: false
  }),
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    logout() {
      this.token = null
      this.currentUser = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      navigateTo('/auth')
    },
    async initAuth() {
      if (this.token) {
        try {
          const res = await fetch(`http://${window.location.hostname}:8000/api/me`, {
            headers: {
              'Authorization': `Bearer ${this.token}`
            }
          })
          if (res.ok) {
            this.currentUser = await res.json()
            this.isAuthenticated = true
          } else {
            this.logout()
          }
        } catch (e) {
          this.logout()
        }
      }
    }
  },
  getters: {
    canAccessAdmin: (state) => {
      return state.currentUser?.role === 'admin' || state.currentUser?.role === 'super_admin'
    }
  }
})

