<script setup>
import { ref, onMounted, shallowRef } from 'vue'
// 核心：引入 Monaco Editor 组件
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'

// --- 状态变量定义 ---
const problemList = ref([])
const selectedProblemId = ref('')
const selectedLanguage = ref('cpp')
const sourceCode = ref(`#include <bits/stdc++.h>
using namespace std;
int main() {

}`)

const mockUserId = ref(1)
const submissionId = ref(null)
const judgerStatus = ref('')
const isSubmitting = ref(false)

// Monaco Editor 的专属配置
const editorOptions = shallowRef({
  theme: 'vs-dark',       // 极客暗黑主题
  fontSize: 16,           // 舒适的字号
  automaticLayout: true,  // 自动自适应大小
  minimap: { enabled: false }, // 关闭右侧的小地图（节省空间）
  scrollBeyondLastLine: false, // 不允许滚动超过最后一行太多
})

// --- 页面加载时请求题库 ---
onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/problems')
    problemList.value = await response.json()
    if (problemList.value.length > 0) {
      selectedProblemId.value = problemList.value[0].id
    }
  } catch (error) {
    console.error("无法连接后端 API:", error)
  }
})

// --- 点击按钮：提交代码 ---
const handleCommit = async () => {
  if (!selectedProblemId.value) return alert('请先选择一道题目')

  isSubmitting.value = true
  judgerStatus.value = '正在安全提交至队列...'

  try {
    const response = await fetch('http://127.0.0.1:8000/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: mockUserId.value,
        problem_id: parseInt(selectedProblemId.value),
        language: selectedLanguage.value,
        code: sourceCode.value
      })
    })

    const data = await response.json()
    if (response.ok) {
      submissionId.value = data.submission_id
      judgerStatus.value = data.current_status
      startPolling(data.submission_id)
    } else {
      judgerStatus.value = '提交失败: ' + data.detail
      isSubmitting.value = false
    }
  } catch (error) {
    judgerStatus.value = '网络异常，无法连接评测服务器'
    isSubmitting.value = false
  }
}

// --- 核心机制：长轮询状态机 ---
const startPolling = (subId) => {
  const timer = setInterval(async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/submissions/${subId}`)
      const data = await response.json()

      if (response.ok) {
        judgerStatus.value = data.status
        if (data.status !== 'Pending') {
          clearInterval(timer)
          isSubmitting.value = false
        }
      }
    } catch (err) {
      console.error("轮询出错:", err)
      clearInterval(timer)
      isSubmitting.value = false
    }
  }, 1000)
}
</script>

<template>
  <div class="oj-workspace">
    <div class="panel left-panel">
      <h2>=== 题库选择 ===</h2>
      <select v-model="selectedProblemId" class="problem-select">
        <option v-for="prob in problemList" :key="prob.id" :value="prob.id">
          #{{ prob.id }} - {{ prob.title }} [{{ prob.difficulty }}]
        </option>
      </select>

      <div class="problem-body">
        <h3>题目描述</h3>
        <p>输入两个整数 A 和 B，计算它们的和并输出。</p>
        <p><strong>输入格式：</strong> 一行两个整数。</p>
        <p><strong>输出格式：</strong> 一行一个整数。</p>
      </div>
    </div>

    <div class="panel right-panel">
      <div class="editor-header">
        <span class="title">Code Editor</span>
        <select v-model="selectedLanguage" class="lang-select">
          <option value="cpp">C++</option>
          <option value="python">Python</option>
        </select>
      </div>

      <div class="editor-container">
        <vue-monaco-editor
          v-model:value="sourceCode"
          :language="selectedLanguage"
          :options="editorOptions"
        />
      </div>

      <div class="console-box">
        <button
          @click="handleCommit"
          :disabled="isSubmitting"
          :class="['submit-btn', { 'btn-disabled': isSubmitting }]"
        >
          {{ isSubmitting ? '评测中...' : '提交代码' }}
        </button>

        <div v-if="judgerStatus" class="status-card">
          <p>提交流水号: <span class="text-highlight">#{{ submissionId }}</span></p>
          <p>评测状态:
            <span :class="['badge', { 'badge-pending': judgerStatus === 'Pending', 'badge-ac': judgerStatus === 'AC' }]">
              {{ judgerStatus }}
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.oj-workspace {
  display: flex;
  gap: 20px;
  max-width: 1200px;
  margin: 30px auto;
  font-family: 'Courier New', Courier, monospace;
  height: 85vh; /* 增加一点高度 */
}
.panel {
  flex: 1;
  border: 2px solid #333;
  border-radius: 8px;
  padding: 20px;
  background-color: #fafafa;
  display: flex;
  flex-direction: column;
}
.problem-select, .lang-select {
  padding: 8px;
  font-size: 16px;
  border: 2px solid #333;
  border-radius: 4px;
  margin-bottom: 15px;
}
.problem-body {
  border-top: 1px dashed #ccc;
  margin-top: 10px;
  line-height: 1.6;
}
.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
/* 给编辑器留出明确的生长空间 */
.editor-container {
  flex: 1;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #444;
}
.console-box {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #eee;
  padding: 15px;
  border-radius: 6px;
}
.submit-btn {
  background-color: #007acc;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
.submit-btn:hover { background-color: #005999; }
.btn-disabled { background-color: #999 !important; cursor: not-allowed; }
.status-card { text-align: right; font-size: 14px; }
.text-highlight { color: #007acc; font-weight: bold; }
.badge { padding: 4px 10px; border-radius: 4px; font-weight: bold; }
.badge-pending { background-color: #ffe58f; color: #d46b08; }
.badge-ac { background-color: #b7eb8f; color: #389e0d; }
</style>