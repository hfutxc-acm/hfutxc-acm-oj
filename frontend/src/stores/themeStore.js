import { reactive, watch } from 'vue'

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

export const themeStore = reactive({
  currentTheme: getStoredTheme()
})

export function toggleTheme() {
  themeStore.currentTheme = themeStore.currentTheme === 'dark' ? 'light' : 'dark'
}

// Watch theme changes and apply it to document root class list
watch(() => themeStore.currentTheme, (newTheme) => {
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
