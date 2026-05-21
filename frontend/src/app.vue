<script setup>
import { ref, onMounted, shallowRef, computed } from 'vue'
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'

// --- 状态变量定义 ---
const problemList = ref([])
const selectedProblemId = ref('')
const selectedLanguage = ref('cpp')
const sourceCode = ref(`// 你的代码...
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b;
    return 0;
}`)

const mockUserId = ref(1)
const submissionId = ref(null)
const judgerStatus = ref('')
const isSubmitting = ref(false)
const historyList = ref([]) // 新增：用于存放历史提交记录的数组

const editorOptions = shallowRef({
  theme: 'vs-dark',
  fontSize: 16,
  automaticLayout: true,
  minimap: { enabled: false },
  scrollBeyondLastLine: false,
})

// 💡 魔法 1：利用计算属性，智能匹配当前选中题目的详细信息
const currentProblem = computed(() => {
  if (!selectedProblemId.value) return null
  return problemList.value.find(p => p.id == selectedProblemId.value)
})

// --- 页面初始化时拉取数据 ---
onMounted(async () => {
  await fetchProblems()
  await fetchHistory()
})

const fetchProblems = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/problems')
    problemList.value = await response.json()
    if (problemList.value.length > 0) {
      selectedProblemId.value = problemList.value[0].id
    }
  } catch (error) { console.error("题库加载失败:", error) }
}

// 💡 魔法 2：获取历史提交记录列表
const fetchHistory = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/submissions')
    if (response.ok) {
      historyList.value = await response.json()
    }
  } catch (error) { console.error("历史记录加载失败:", error) }
}

// --- 核心提交逻辑 ---
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
      fetchHistory() // 提交成功立刻刷新一下列表，展示出刚插入的 Pending 记录
      startPolling(data.submission_id)
    } else {
      judgerStatus.value = '提交失败: ' + data.detail
      isSubmitting.value = false
    }
  } catch (error) {
    judgerStatus.value = '网络异常'
    isSubmitting.value = false
  }
}

// --- Monaco 编辑器挂载时，加入手写的智能提示 ---
const handleEditorMount = (editor, monaco) => {
  monaco.languages.registerCompletionItemProvider('cpp', {
    triggerCharacters: ['.', ':'],
    provideCompletionItems: (model, position) => {
      const suggestions = [
        { label: 'std::cin', kind: monaco.languages.CompletionItemKind.Function, insertText: 'cin >> ' },
        { label: 'std::cout', kind: monaco.languages.CompletionItemKind.Function, insertText: 'cout << ' },
        { label: 'std::endl', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'endl;' },
        { label: 'include_iostream', kind: monaco.languages.CompletionItemKind.Snippet, insertText: '#include <iostream>\nusing namespace std;\n' },
        { label: 'main_template', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'int main() {\n\t${1}\n\treturn 0;\n}', insertTextRules: monaco.languages.CompletionItemInsertRule.InsertAsSnippet }
      ]
      return { suggestions }
    }
  })
}

// --- 状态轮询 ---
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
          fetchHistory() // 💡 评测完成后，再次刷新底部表格，让结果绿起来或红起来！
        }
      }
    } catch (err) {
      clearInterval(timer)
      isSubmitting.value = false
    }
  }, 1000)
}

// 帮助函数：格式化时间显示
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const d = new Date(timeStr)
  return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}:${d.getSeconds().toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="oj-container">
    <div class="oj-workspace">
      <div class="panel left-panel">
        <h2>=== 题库选择 ===</h2>
        <select v-model="selectedProblemId" class="problem-select">
          <option v-for="prob in problemList" :key="prob.id" :value="prob.id">
            #{{ prob.id }} - {{ prob.title }} [{{ prob.difficulty }}]
          </option>
        </select>

        <div class="problem-body" v-if="currentProblem">
          <h3>题目描述</h3>
          <p>{{ currentProblem.description || "管理员太懒了，还没有写题目描述..." }}</p>
          <div v-if="currentProblem.id === 1" class="mock-desc">
            <p><strong>输入格式：</strong> 一行两个整数。</p>
            <p><strong>输出格式：</strong> 一行一个整数。</p>
          </div>
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

        <div class="editor-container">
          <vue-monaco-editor
            v-model:value="sourceCode"
            :language="selectedLanguage"
            :options="editorOptions"
            @mounting="handleEditorMount"
          />
        </div>

        <div class="console-box">
          <button @click="handleCommit" :disabled="isSubmitting" :class="['submit-btn', { 'btn-disabled': isSubmitting }]">
            {{ isSubmitting ? '评测中...' : '提交代码' }}
          </button>
          <div v-if="judgerStatus" class="status-card">
            <p>当前提交流水号: <span class="text-highlight">#{{ submissionId }}</span></p>
            <p>实时状态:
              <span :class="['badge', { 'badge-pending': judgerStatus === 'Pending', 'badge-ac': judgerStatus === 'AC', 'badge-error': ['WA', 'CE', 'RE', 'TLE'].includes(judgerStatus) }]">
                {{ judgerStatus }}
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="history-panel">
      <h3>=== 最新评测记录 ===</h3>
      <table class="history-table">
        <thead>
          <tr>
            <th>运行 ID</th>
            <th>题目 ID</th>
            <th>语言</th>
            <th>提交时间</th>
            <th>评测状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in historyList" :key="sub.id">
            <td class="col-id">#{{ sub.id }}</td>
            <td>Problem {{ sub.problem_id }}</td>
            <td class="col-lang">{{ sub.language }}</td>
            <td class="col-time">{{ formatTime(sub.created_at) }}</td>
            <td class="col-status">
              <span :class="['status-text', { 'is-ac': sub.status === 'AC', 'is-pending': sub.status === 'Pending', 'is-err': ['WA', 'CE', 'RE', 'TLE'].includes(sub.status) }]">
                {{ sub.status }}
              </span>
            </td>
          </tr>
          <tr v-if="historyList.length === 0">
            <td colspan="5" style="text-align: center; color: #888;">暂无提交记录，去拿下你的第一个 AC 吧！</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.oj-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 0;
  font-family: 'Courier New', Courier, monospace;
}
.oj-workspace {
  display: flex;
  gap: 20px;
  height: 65vh; /* 稍微压缩高度给下面的表格腾地方 */
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
.problem-select, .lang-select { padding: 8px; font-size: 16px; border: 2px solid #333; border-radius: 4px; margin-bottom: 15px; }
.problem-body { border-top: 1px dashed #ccc; margin-top: 10px; line-height: 1.6; padding-top: 10px;}
.mock-desc { margin-top: 15px; background: #eee; padding: 10px; border-radius: 4px;}
.editor-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.editor-container { flex: 1; border-radius: 6px; overflow: hidden; border: 1px solid #444; }
.console-box { margin-top: 15px; display: flex; justify-content: space-between; align-items: center; background: #eee; padding: 15px; border-radius: 6px; }
.submit-btn { background-color: #007acc; color: white; border: none; padding: 12px 24px; font-size: 16px; font-weight: bold; border-radius: 4px; cursor: pointer; }
.submit-btn:hover { background-color: #005999; }
.btn-disabled { background-color: #999 !important; cursor: not-allowed; }
.status-card { text-align: right; font-size: 14px; }
.badge { padding: 4px 10px; border-radius: 4px; font-weight: bold; }
.badge-pending { background-color: #ffe58f; color: #d46b08; }
.badge-ac { background-color: #b7eb8f; color: #389e0d; }
.badge-error { background-color: #ffa39e; color: #a8071a; }

/* 历史记录表格样式 */
.history-panel {
  margin-top: 20px;
  border: 2px solid #333;
  border-radius: 8px;
  padding: 20px;
  background-color: #fafafa;
}
.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}
.history-table th, .history-table td {
  padding: 12px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}
.history-table th { background-color: #eee; font-weight: bold; }
.history-table tbody tr:hover { background-color: #f5f5f5; }
.col-id { font-weight: bold; color: #555; }
.col-lang { font-family: monospace; background: #eaeaea; padding: 2px 6px; border-radius: 4px; }
.col-time { color: #888; font-size: 14px; }
.status-text { font-weight: bold; }
.is-ac { color: #389e0d; }
.is-pending { color: #d46b08; }
.is-err { color: #cf1322; }
</style>