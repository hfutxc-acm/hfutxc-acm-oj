<script setup>
import { ref, onMounted } from 'vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getProblems } from '../api/problems'
import { currentRoute, navigateTo } from '../router'

const text = ref('')
const title = ref('')
const selectedProblemId = ref(currentRoute.value.query.pid || '')
const problems = ref([])
const submitting = ref(false)
const message = ref('')

onMounted(async () => {
  problems.value = await getProblems()
})

async function submit() {
  if (!selectedProblemId.value) {
    message.value = '请选择关联的题目'
    return
  }
  if (!title.value.trim()) {
    message.value = '请输入题解标题'
    return
  }
  if (!text.value.trim()) {
    message.value = '请输入题解内容'
    return
  }
  
  submitting.value = true
  message.value = '提交中...'
  
  // mock submit logic
  setTimeout(() => {
    submitting.value = false
    message.value = '提交成功！'
    setTimeout(() => {
      navigateTo(`/problems/${selectedProblemId.value}/solutions`)
    }, 1000)
  }, 800)
}
</script>
<template>
  <div class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Solutions / Publish</p>
      <h1>发布题解</h1>
      <p>分享你的思路与代码，帮助更多人进步。</p>
    </div>
    
    <div class="panel">
      <div class="form-row">
        <label class="form-label">关联题目</label>
        <select v-model="selectedProblemId" class="control">
          <option value="" disabled>请选择关联的题目...</option>
          <option v-for="p in problems" :key="p.id" :value="p.id">
            #{{ p.id }} - {{ p.title }}
          </option>
        </select>
      </div>

      <div class="form-row">
        <label class="form-label">题解标题</label>
        <input v-model="title" class="control" placeholder="请输入直观且吸引人的标题" />
      </div>
      
      <div class="editor-wrapper">
        <MdEditor v-model="text" class="md-editor" :toolbarsExclude="['github']" />
      </div>

      <div class="action-row" style="margin-top: 20px;">
        <button class="primary-btn" :disabled="submitting" @click="submit">
          {{ submitting ? '提交中...' : '提交发布' }}
        </button>
        <span v-if="message" class="form-message" :class="{'error': message.includes('请')}">{{ message }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.form-row {
  margin-bottom: 20px;
}
.form-label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--text);
}
.editor-wrapper {
  margin-top: 10px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
}
.md-editor {
  height: 600px;
}
.form-message {
  margin-left: 15px;
  color: var(--success);
}
.form-message.error {
  color: var(--danger);
}
</style>
