<script setup>
import { ref, watch, reactive, computed, shallowRef, nextTick } from 'vue'
import { submitCode } from '../../api/problems'
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'
import { templates, registerVscodeDarkTheme, registerCustomCompletions } from '../../utils/monacoCustomizer'
import { themeStore } from '../../stores/themeStore'

const props = defineProps({
  problemId: [String, Number]
})

const emit = defineEmits(['submitted'])

const language = ref('cpp')
const showSettings = ref(false)
const editorRef = shallowRef()

// Editor Settings with LocalStorage persistence
const DEFAULT_SETTINGS = {
  theme: 'vscode-dark',
  fontSize: 14,
  tabSize: 4
}

const getStoredSettings = () => {
  try {
    const stored = localStorage.getItem('oj-editor-settings')
    return stored ? JSON.parse(stored) : DEFAULT_SETTINGS
  } catch {
    return DEFAULT_SETTINGS
  }
}

const settings = reactive(getStoredSettings())

watch(settings, (newSettings) => {
  try {
    localStorage.setItem('oj-editor-settings', JSON.stringify(newSettings))
  } catch (e) {
    console.error('Failed to save editor settings', e)
  }
}, { deep: true })

// Sync editor theme with global light/dark mode changes
watch(() => themeStore.currentTheme, (newGlobalTheme) => {
  if (newGlobalTheme === 'light' && (settings.theme === 'vscode-dark' || settings.theme === 'vs-dark' || settings.theme === 'hc-black')) {
    settings.theme = 'vs'
  } else if (newGlobalTheme === 'dark' && settings.theme === 'vs') {
    settings.theme = 'vscode-dark'
  }
})

const code = ref(templates.cpp)
const message = ref('')
const saving = ref(false)

// Automatically switch templates if current code matches default or is empty
watch(language, (newLang, oldLang) => {
  const oldTemplate = templates[oldLang]?.trim()
  const currentCode = code.value?.trim() || ''
  if (!currentCode || currentCode === oldTemplate) {
    code.value = templates[newLang]
  }
})

const editorOptions = computed(() => ({
  automaticLayout: true,
  minimap: { enabled: false },
  fontSize: settings.fontSize,
  fontFamily: 'ui-monospace, SFMono-Regular, Consolas, monospace',
  lineNumbers: 'on',
  scrollbar: {
    vertical: 'visible',
    horizontal: 'visible',
    useShadows: false,
    verticalScrollbarSize: 10,
    horizontalScrollbarSize: 10,
  },
  cursorBlinking: 'smooth',
  cursorSmoothCaretAnimation: 'on',
  smoothScrolling: true,
  tabSize: settings.tabSize,
  insertSpaces: true,
  detectIndentation: false,
  padding: {
    top: 12,
    bottom: 12
  },
  renderLineHighlight: 'all',
  quickSuggestions: {
    other: true,
    comments: false,
    strings: false
  }
}))

// Function to update Monaco Editor model options dynamically
const updateModelOptions = (editor) => {
  if (!editor) return
  const model = editor.getModel()
  if (model) {
    model.updateOptions({
      tabSize: settings.tabSize,
      insertSpaces: true,
      detectIndentation: false
    })
  }
}

const handleMount = (editorInstance, monacoInstance) => {
  editorRef.value = editorInstance

  // Register VS Code custom theme and completions from monacoCustomizer
  registerVscodeDarkTheme(monacoInstance)
  registerCustomCompletions(monacoInstance)

  updateModelOptions(editorInstance)
}

// Watch tabSize changes and update model configuration immediately
watch(() => settings.tabSize, () => {
  updateModelOptions(editorRef.value)
})

// Ensure settings are also applied when language or model swaps
watch(language, async () => {
  await nextTick()
  // 给 Monaco 一点时间完成 model 切换
  setTimeout(() => {
    updateModelOptions(editorRef.value)
  }, 0)
})

async function handleSubmit() {
  if (!props.problemId) return
  
  const trimmedCode = code.value?.trim()
  if (!trimmedCode) {
    message.value = '代码不能为空'
    return
  }

  saving.value = true
  message.value = '提交中...'
  try {
    const result = await submitCode({
      userId: 1, // TODO: 从用户状态存储中获取实际 ID
      problemId: props.problemId,
      language: language.value,
      code: trimmedCode
    })
    message.value = `提交成功，运行 ID #${result.submission_id}`
    emit('submitted', result)
  } catch (error) {
    message.value = error.message
  } finally {
    saving.value = false
  }
}

function resetCode() {
  code.value = templates[language.value]
  message.value = ''
}
</script>

<template>
  <section class="submit-panel">
    <div class="section-title-row">
      <h2>提交代码</h2>
      <div class="controls-row">
        <select v-model="language" class="control compact-control">
          <option value="cpp">C++17</option>
          <option value="c">C</option>
          <option value="python">Python 3</option>
          <option value="java">Java 11</option>
          <option value="go">Go</option>
          <option value="rust">Rust</option>
          <option value="javascript">JavaScript</option>
          <option value="csharp">C#</option>
          <option value="kotlin">Kotlin</option>
        </select>
        <button class="ghost-btn settings-btn" :class="{ active: showSettings }" @click="showSettings = !showSettings">
          <span class="icon">⚙️</span> 设置
        </button>
      </div>
    </div>

    <!-- Collapsible Settings Panel -->
    <transition name="slide">
      <div v-if="showSettings" class="editor-settings-panel">
        <div class="setting-item">
          <label>编辑器主题</label>
          <select v-model="settings.theme" class="control">
            <option value="vscode-dark">VS Code 深色 (vscode-dark)</option>
            <option value="vs-dark">内置深色 (vs-dark)</option>
            <option value="vs">内置浅色 (vs)</option>
            <option value="hc-black">高对比度 (hc-black)</option>
          </select>
        </div>
        <div class="setting-item">
          <label>字体大小</label>
          <select v-model="settings.fontSize" class="control">
            <option :value="12">12 px</option>
            <option :value="14">14 px</option>
            <option :value="16">16 px</option>
            <option :value="18">18 px</option>
            <option :value="20">20 px</option>
          </select>
        </div>
        <div class="setting-item">
          <label>缩进空格</label>
          <select v-model="settings.tabSize" class="control">
            <option :value="2">2 个空格</option>
            <option :value="4">4 个空格</option>
            <option :value="8">8 个空格</option>
          </select>
        </div>
      </div>
    </transition>

    <div class="code-editor-container" :class="settings.theme">
      <VueMonacoEditor
        v-model:value="code"
        :language="language"
        :theme="settings.theme"
        :options="editorOptions"
        @mount="handleMount"
      />
    </div>
    <div class="action-row">
      <button class="primary-btn" :disabled="saving" @click="handleSubmit">{{ saving ? '提交中...' : '提交' }}</button>
      <button class="ghost-btn" @click="resetCode">重置</button>
      <span v-if="message" class="form-message">{{ message }}</span>
    </div>
  </section>
</template>

<style scoped>
.controls-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.settings-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  min-height: 38px;
  padding: 0 12px;
  transition: all 0.2s ease;
}

.settings-btn.active {
  background: var(--primary-dark);
  color: #ffffff;
  border-color: var(--primary-dark);
}

.editor-settings-panel {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  background: var(--panel-soft);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02);
}

.setting-item {
  display: grid;
  gap: 6px;
}

.setting-item label {
  font-size: 12px;
  font-weight: 800;
  color: var(--muted);
}

.code-editor-container {
  width: 100%;
  height: 420px;
  border: 1px solid #1e293b;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 14px;
  margin-bottom: 14px;
  transition: border-color 0.2s, background-color 0.2s;
}

.code-editor-container.vscode-dark,
.code-editor-container.vs-dark {
  border-color: #1e293b;
  background: #1e1e1e;
}

.code-editor-container.vs {
  border-color: #cbd5e1;
  background: #ffffff;
}

.code-editor-container.hc-black {
  border-color: #ffffff;
  background: #000000;
}

/* Slide Transition */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 120px;
  opacity: 1;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
  padding-top: 0;
  padding-bottom: 0;
  margin-top: 0;
}

@media (max-width: 600px) {
  .editor-settings-panel {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}
</style>
