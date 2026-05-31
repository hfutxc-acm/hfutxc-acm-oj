import { useAuthStore } from '../stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || `http://${window.location.hostname}:8000`

export async function request(path, options = {}) {
  const headers = {
    ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
    ...(options.headers || {})
  }

  if (useAuthStore().token) {
    headers['Authorization'] = `Bearer ${useAuthStore().token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers
  })

  let data = null
  try {
    data = await response.json()
  } catch {
    data = null
  }

  if (!response.ok) {
    if (response.status === 401 && useAuthStore().isAuthenticated) {
      useAuthStore()
    }
    const message = data?.detail || data?.message || `请求失败：${response.status}`
    throw new Error(Array.isArray(message) ? message.map(item => item.msg).join('; ') : message)
  }

  return data
}

export { API_BASE_URL }
