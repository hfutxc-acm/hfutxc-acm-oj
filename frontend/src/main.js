import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { config } from 'md-editor-v3'
import katex from 'katex'
import 'katex/dist/katex.min.css'

// Configure md-editor-v3 to use the local katex instance instead of CDN
config({
  editorExtensions: {
    katex: {
      instance: katex
    }
  }
})

createApp(App).mount('#app')
