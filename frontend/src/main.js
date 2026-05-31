import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import { config } from 'md-editor-v3'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import { useAuthStore } from './stores/authStore.js'

// Configure md-editor-v3 to use the local katex instance instead of CDN
config({
  editorExtensions: {
    katex: {
      instance: katex
    }
  }
})

function applyPrimaryColor() {
  try {
    const savedColor = localStorage.getItem('custom-primary-color')
    if (savedColor) {
      document.documentElement.setAttribute('data-primary-color', savedColor)
    } else {
      document.documentElement.removeAttribute('data-primary-color')
    }
  } catch (e) {
    console.error(e)
  }
}
applyPrimaryColor()

// Listen to storage events to instantly sync theme colors when changed in other tabs/pages
window.addEventListener('storage', (e) => {
  if (e.key === 'custom-primary-color') {
    applyPrimaryColor()
  }
})

const pinia = createPinia()
const app = createApp(App)
app.use(pinia)

useAuthStore().initAuth().then(() => {
  app.mount('#app')
})
