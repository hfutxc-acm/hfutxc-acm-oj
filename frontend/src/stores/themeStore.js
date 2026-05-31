import { watch, ref } from 'vue'
import { defineStore } from 'pinia'

const getStoredTheme = () => {
  try {
    const stored = localStorage.getItem('oj-theme')
    if (stored) return stored
    // Default to system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  } catch {
    return 'light'
  }
}

export const useThemeStore = defineStore('theme', () => {
  const currentTheme = ref(getStoredTheme())

  function toggleTheme() {
    currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
  }

  // Watch theme changes and apply it to document root class list
  watch(currentTheme, (newTheme) => {
    const root = document.documentElement
    if (newTheme === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    try {
      localStorage.setItem('oj-theme', newTheme)
    } catch (e) {
      console.error('Failed to save theme preference', e)
    }
  }, { immediate: true })

  return {
    currentTheme,
    toggleTheme
  }
})
