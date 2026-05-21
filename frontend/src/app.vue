<script setup>
import { ref, onMounted } from 'vue'

// --- 状态变量定义 ---
const problemList = ref([])         // 题库列表
const selectedProblemId = ref('')   // 选中的题目 ID
const selectedLanguage = ref('cpp') // 选中的编程语言
const sourceCode = ref(`// 请在此处输入你的 A+B 代码
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b;
    return 0;
}`)

const mockUserId = ref(1)          // 假定当前登录用户 ID 为 1 (刚才我们在 database 注入过)
const submissionId = ref(null)     // 提交后拿到的流水号
const judgerStatus = ref('')       // 动态评测状态：Pending -> AC
const isSubmitting = ref(false)    // 按钮防止重复点击状态

// --- 1. 页面加载时请求题库 ---
onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/problems')
    problemList.value = await response.json()
    // 默认选中第一道题
    if (problemList.value.length > 0) {
      selectedProblemId.value = problemList.value[0].id
    }
  } catch (error) {
    console.error("无法连接后端 API:", error)
  }
})

// --- 2. 点击按钮：提交代码 ---
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
      judgerStatus.value = data.current_status // 此时拿到的是 "Pending"

      // 开启魔法：每隔 1 秒向后端查一次状态
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

// --- 3. 核心机制：长轮询状态机 ---
const startPolling = (subId) => {
  const timer = setInterval(async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/submissions/${subId}`)
      const data = await response.json()

      if (response.ok) {
        // 更新网页上的状态字眼
        judgerStatus.value = data.status

        // 如果状态不再是 Pending（说明评测机跑完了，变成了 AC 或是 WA）
        if (data.status !== 'Pending') {
          clearInterval(timer)     // 💥 停止轮询，释放内存
          isSubmitting.value = false // 恢复按钮点击
        }
      }
    } catch (err) {
      console.error("轮询出错:", err)
      clearInterval(timer)
      isSubmitting.value = false
    }
  }, 1000) // 每 1000 毫秒（1秒）侦听一次
}
</script>

<template>
  <div class="oj-workspace">
    <div class="panel left-panel">
      <h2>=== 题库选择 ===</h2>
      <select v-model="selectedProblemId" class="problem-select">
        <option v-for="prob in problemList" :key="prob.id" :value="prob.id">
          #{ { prob.id } } - { { prob.title } } [{ { prob.difficulty } }]
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
          <option value="cpp">C++ 17</option>
          <option value="python">Python 3.12</option>
        </select>
      </div>

      <textarea v-model="sourceCode" class="code-textarea" spellcheck="false"></textarea>

      <div class="console-box">
        <button
          @click="handleCommit"
          :disabled="isSubmitting"
          :class="['submit-btn', { 'btn-disabled': isSubmitting }]"
        >
          { { isSubmitting ? '评测中...' : '提交代码' } }
        </button>

        <div v-if="judgerStatus" class="status-card">
          <p>提交流水号: <span class="text-highlight">#{ { submissionId } }</span></p>
          <p>评测状态:
            <span :class="['badge', { 'badge-pending': judgerStatus === 'Pending', 'badge-ac': judgerStatus === 'AC' }]">
              { { judgerStatus } }
            </span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 现代双栏极客分屏布局 */
.oj-workspace {
  display: flex;
  gap: 20px;
  max-width: 1200px;
  margin: 30px auto;
  font-family: 'Courier New', Courier, monospace;
  height: 80vh;
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
.code-textarea {
  flex: 1;
  background-color: #1e1e1e;
  color: #7ec699;
  padding: 15px;
  font-family: consolas, Monaco, monospace;
  font-size: 15px;
  border-radius: 6px;
  resize: none;
  border: none;
  line-height: 1.4;
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
.badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: bold;
}
.badge-pending { background-color: #ffe58f; color: #d46b08; }
.badge-ac { background-color: #b7eb8f; color: #389e0d; }
</style>