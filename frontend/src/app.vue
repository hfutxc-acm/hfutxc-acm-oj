<script setup>
import { ref, onMounted, onUnmounted, shallowRef, computed } from 'vue'
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
const editingProblemId = ref(null)
const adminMessage = ref('')
const uploadMessage = ref('')
const isSavingProblem = ref(false)
const isUploadingData = ref(false)
const selectedUploadProblemId = ref('')
const selectedZipFile = ref(null)
const testcaseList = ref([])
const currentPage = ref('judge')
const adminForm = ref({
  title: '',
  difficulty: 'Easy',
  description: '',
  input_description: '',
  output_description: '',
  time_limit_ms: 1000,
  memory_limit_mb: 256,
  is_public: true
})

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

const syncPageFromHash = () => {
  currentPage.value = window.location.hash === '#/admin' ? 'admin' : 'judge'
}

const navigateTo = (page) => {
  window.location.hash = page === 'admin' ? '#/admin' : '#/judge'
  syncPageFromHash()
}

// --- 页面初始化时拉取数据 ---
onMounted(async () => {
  if (!window.location.hash) {
    window.location.hash = '#/judge'
  }
  syncPageFromHash()
  window.addEventListener('hashchange', syncPageFromHash)
  await fetchProblems()
  await fetchTestcases()
  await fetchHistory()
})

onUnmounted(() => {
  window.removeEventListener('hashchange', syncPageFromHash)
})

const fetchProblems = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/problems')
    problemList.value = await response.json()
    if (!selectedProblemId.value && problemList.value.length > 0) {
      selectedProblemId.value = problemList.value[0].id
    }
    if (!selectedUploadProblemId.value && problemList.value.length > 0) {
      selectedUploadProblemId.value = problemList.value[0].id
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

const resetAdminForm = () => {
  editingProblemId.value = null
  adminMessage.value = ''
  adminForm.value = {
    title: '',
    difficulty: 'Easy',
    description: '',
    input_description: '',
    output_description: '',
    time_limit_ms: 1000,
    memory_limit_mb: 256,
    is_public: true
  }
}

const editProblem = async (problem) => {
  editingProblemId.value = problem.id
  adminMessage.value = ''
  selectedUploadProblemId.value = problem.id
  adminForm.value = {
    title: problem.title || '',
    difficulty: problem.difficulty || 'Easy',
    description: problem.description || '',
    input_description: problem.input_description || '',
    output_description: problem.output_description || '',
    time_limit_ms: problem.time_limit_ms || 1000,
    memory_limit_mb: problem.memory_limit_mb || 256,
    is_public: problem.is_public !== false
  }
  await fetchTestcases(problem.id)
}

const saveProblem = async () => {
  if (!adminForm.value.title.trim()) {
    adminMessage.value = '请填写题目标题'
    return
  }

  isSavingProblem.value = true
  adminMessage.value = editingProblemId.value ? '正在保存题目...' : '正在创建题目...'
  const payload = {
    ...adminForm.value,
    title: adminForm.value.title.trim(),
    time_limit_ms: Number(adminForm.value.time_limit_ms) || 1000,
    memory_limit_mb: Number(adminForm.value.memory_limit_mb) || 256
  }

  try {
    const url = editingProblemId.value
      ? `http://127.0.0.1:8000/api/admin/problems/${editingProblemId.value}`
      : 'http://127.0.0.1:8000/api/admin/problems'
    const response = await fetch(url, {
      method: editingProblemId.value ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await response.json()

    if (response.ok) {
      const problemId = editingProblemId.value || data.id
      adminMessage.value = editingProblemId.value ? `题目 #${problemId} 已保存` : `题目 #${problemId} 创建成功`
      await fetchProblems()
      selectedProblemId.value = problemId
      selectedUploadProblemId.value = problemId
      if (!editingProblemId.value) {
        editingProblemId.value = problemId
      }
      await fetchTestcases(problemId)
    } else {
      adminMessage.value = '保存失败: ' + (data.detail || '未知错误')
    }
  } catch (error) {
    adminMessage.value = '网络异常，无法保存题目'
  } finally {
    isSavingProblem.value = false
  }
}

const handleZipFileChange = (event) => {
  selectedZipFile.value = event.target.files?.[0] || null
}

const fetchTestcases = async (problemId = selectedUploadProblemId.value) => {
  testcaseList.value = []
  if (!problemId) return
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/admin/problems/${problemId}/testcases`)
    const data = await response.json()
    if (response.ok) {
      testcaseList.value = data
    } else {
      uploadMessage.value = data.detail || '测试点加载失败'
    }
  } catch (error) {
    uploadMessage.value = '网络异常，无法加载测试点'
  }
}

const uploadTestcases = async () => {
  if (!selectedUploadProblemId.value) {
    uploadMessage.value = '请先选择题目'
    return
  }
  if (!selectedZipFile.value) {
    uploadMessage.value = '请选择 zip 文件'
    return
  }

  isUploadingData.value = true
  uploadMessage.value = '正在上传测试数据...'
  const formData = new FormData()
  formData.append('file', selectedZipFile.value)

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/admin/problems/${selectedUploadProblemId.value}/testcases/upload`, {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    if (response.ok) {
      uploadMessage.value = `上传成功，共 ${data.case_count} 个测试点`
      selectedZipFile.value = null
      await fetchProblems()
      await fetchTestcases(selectedUploadProblemId.value)
    } else {
      uploadMessage.value = '上传失败: ' + (data.detail || '未知错误')
    }
  } catch (error) {
    uploadMessage.value = '网络异常，无法上传测试数据'
  } finally {
    isUploadingData.value = false
  }
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
  <main class="oj-page">
    <header class="topbar">
      <div>
        <p class="eyebrow">HFUTXC ACM OJ</p>
        <h1>{{ currentPage === 'admin' ? '题目管理后台' : '在线评测工作台' }}</h1>
      </div>
      <div class="topbar-actions">
        <nav class="page-tabs" aria-label="主导航">
          <button :class="{ active: currentPage === 'judge' }" @click="navigateTo('judge')">评测工作台</button>
          <button :class="{ active: currentPage === 'admin' }" @click="navigateTo('admin')">题目管理</button>
        </nav>
        <div class="topbar-meta">
          <span>{{ problemList.length }} 道题目</span>
          <span>测试用户 #{{ mockUserId }}</span>
        </div>
      </div>
    </header>

    <section v-if="currentPage === 'judge'" class="workspace">
      <aside class="panel problem-panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">Problem</p>
            <h2>题目</h2>
          </div>
          <span v-if="currentProblem" class="difficulty">{{ currentProblem.difficulty }}</span>
        </div>

        <label class="field-label" for="problem-select">题目列表</label>
        <select id="problem-select" v-model="selectedProblemId" class="control problem-select">
          <option value="" disabled>请选择题目</option>
          <option v-for="prob in problemList" :key="prob.id" :value="prob.id">
            #{{ prob.id }} - {{ prob.title }} ({{ prob.testcase_count || 0 }})
          </option>
        </select>

        <div v-if="currentProblem" class="problem-body">
          <div class="problem-title-row">
            <h3>{{ currentProblem.title }}</h3>
            <span>#{{ currentProblem.id }}</span>
          </div>
          <p>{{ currentProblem.description || "暂无题目描述。" }}</p>

          <div class="format-box">
            <div>
              <strong>输入格式</strong>
              <p>{{ currentProblem.input_description || '暂无输入格式。' }}</p>
            </div>
            <div>
              <strong>输出格式</strong>
              <p>{{ currentProblem.output_description || '暂无输出格式。' }}</p>
            </div>
            <div>
              <strong>限制</strong>
              <p>{{ currentProblem.time_limit_ms }} ms / {{ currentProblem.memory_limit_mb }} MB</p>
            </div>
            <div>
              <strong>测试点</strong>
              <p>{{ currentProblem.testcase_count || 0 }} 个</p>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">暂无题目，请先在题目管理中创建。</div>
      </aside>

      <section class="panel editor-panel">
        <div class="section-head editor-toolbar">
          <div>
            <p class="eyebrow">Editor</p>
            <h2>代码编辑</h2>
          </div>
          <select v-model="selectedLanguage" class="control lang-select">
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

        <footer class="submit-bar">
          <button @click="handleCommit" :disabled="isSubmitting" class="submit-btn">
            {{ isSubmitting ? '评测中...' : '提交代码' }}
          </button>
          <div class="status-card" :class="{ muted: !judgerStatus }">
            <span>流水号 {{ submissionId ? `#${submissionId}` : '-' }}</span>
            <span
              :class="['badge', {
                'badge-pending': judgerStatus === 'Pending',
                'badge-ac': judgerStatus === 'AC',
                'badge-error': ['WA', 'CE', 'RE', 'TLE'].includes(judgerStatus)
              }]"
            >
              {{ judgerStatus || '未提交' }}
            </span>
          </div>
        </footer>
      </section>
    </section>

    <section v-if="currentPage === 'admin'" class="admin-page">
      <section class="panel admin-panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">Admin</p>
            <h2>{{ editingProblemId ? `编辑题目 #${editingProblemId}` : '新增题目' }}</h2>
          </div>
        </div>
        <form class="admin-form" @submit.prevent="saveProblem">
          <label class="form-field">
            <span>标题</span>
            <input
              v-model="adminForm.title"
              class="control"
              type="text"
              placeholder="例如：A+B Problem"
            />
          </label>
          <label class="form-field">
            <span>难度</span>
            <select v-model="adminForm.difficulty" class="control">
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </label>
          <label class="form-field span-all">
            <span>描述</span>
            <textarea
              v-model="adminForm.description"
              class="control admin-textarea"
              placeholder="输入题面描述"
            ></textarea>
          </label>
          <label class="form-field span-all">
            <span>输入格式</span>
            <textarea
              v-model="adminForm.input_description"
              class="control small-textarea"
              placeholder="例如：一行两个整数 a,b。"
            ></textarea>
          </label>
          <label class="form-field span-all">
            <span>输出格式</span>
            <textarea
              v-model="adminForm.output_description"
              class="control small-textarea"
              placeholder="例如：一行一个整数，表示 a+b。"
            ></textarea>
          </label>
          <label class="form-field">
            <span>时间限制 ms</span>
            <input v-model.number="adminForm.time_limit_ms" class="control" type="number" min="100" />
          </label>
          <label class="form-field">
            <span>内存限制 MB</span>
            <input v-model.number="adminForm.memory_limit_mb" class="control" type="number" min="16" />
          </label>
          <label class="check-field span-all">
            <input v-model="adminForm.is_public" type="checkbox" />
            <span>公开题目</span>
          </label>
          <div class="admin-actions span-all">
            <button class="admin-btn" type="submit" :disabled="isSavingProblem">
              {{ isSavingProblem ? '保存中...' : (editingProblemId ? '保存修改' : '新增题目') }}
            </button>
            <button class="ghost-btn" type="button" @click="resetAdminForm">清空表单</button>
          </div>
        </form>
        <p v-if="adminMessage" class="admin-message">{{ adminMessage }}</p>
      </section>

      <section class="panel upload-panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">Test Data</p>
            <h2>上传测试数据</h2>
          </div>
        </div>
        <div class="upload-form">
          <label class="form-field">
            <span>选择题目</span>
            <select v-model="selectedUploadProblemId" class="control" @change="fetchTestcases(selectedUploadProblemId)">
              <option value="" disabled>请选择题目</option>
              <option v-for="prob in problemList" :key="prob.id" :value="prob.id">
                #{{ prob.id }} - {{ prob.title }} ({{ prob.testcase_count || 0 }} 个测试点)
              </option>
            </select>
          </label>
          <label class="form-field">
            <span>测试数据 zip</span>
            <input class="control file-control" type="file" accept=".zip" @change="handleZipFileChange" />
          </label>
          <button class="admin-btn" type="button" :disabled="isUploadingData" @click="uploadTestcases">
            {{ isUploadingData ? '上传中...' : '上传测试数据 zip' }}
          </button>
          <p v-if="uploadMessage" class="admin-message">{{ uploadMessage }}</p>
        </div>

        <div class="case-list">
          <h3>当前测试点</h3>
          <div v-if="testcaseList.length === 0" class="empty-state">暂无测试点。</div>
          <div v-for="caseItem in testcaseList" :key="caseItem.id" class="case-item">
            <span>#{{ caseItem.sort_order }}</span>
            <code>{{ caseItem.input_path }}</code>
            <code>{{ caseItem.output_path }}</code>
          </div>
        </div>
      </section>

      <section class="panel problem-list-panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">Problems</p>
            <h2>题目列表</h2>
          </div>
        </div>

        <div class="problem-list">
          <article v-for="prob in problemList" :key="prob.id" class="problem-item">
            <div>
              <h3>#{{ prob.id }} {{ prob.title }}</h3>
              <p>{{ prob.description || '暂无题目描述。' }}</p>
              <small>{{ prob.testcase_count || 0 }} 个测试点 · {{ prob.time_limit_ms }} ms · {{ prob.memory_limit_mb }} MB</small>
            </div>
            <div class="problem-item-actions">
              <span class="difficulty">{{ prob.difficulty }}</span>
              <button class="ghost-btn" type="button" @click="editProblem(prob)">编辑</button>
            </div>
          </article>
          <div v-if="problemList.length === 0" class="empty-state">暂无题目。</div>
        </div>
      </section>
    </section>

    <section v-if="currentPage === 'judge'" class="submissions-section">
      <section class="panel history-panel">
        <div class="section-head">
          <div>
            <p class="eyebrow">Submissions</p>
            <h2>最新评测记录</h2>
          </div>
        </div>

        <div class="table-wrap">
          <table class="history-table">
            <thead>
              <tr>
                <th>运行 ID</th>
                <th>题目 ID</th>
                <th>语言</th>
                <th>提交时间</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sub in historyList" :key="sub.id">
                <td class="col-id">#{{ sub.id }}</td>
                <td>Problem {{ sub.problem_id }}</td>
                <td><span class="lang-pill">{{ sub.language }}</span></td>
                <td class="col-time">{{ formatTime(sub.created_at) }}</td>
                <td>
                  <span :class="['status-text', { 'is-ac': sub.status === 'AC', 'is-pending': sub.status === 'Pending', 'is-err': ['WA', 'CE', 'RE', 'TLE'].includes(sub.status) }]">
                    {{ sub.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="historyList.length === 0">
                <td colspan="5" class="empty-row">暂无提交记录</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </section>
  </main>
</template>

<style scoped>
.oj-page {
  width: min(1440px, 100%);
  margin: 0 auto;
  padding: 24px;
}

.topbar {
  align-items: center;
  display: flex;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 20px;
}

.topbar-actions {
  align-items: flex-end;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.page-tabs {
  background: #e2e8f0;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  display: inline-flex;
  gap: 4px;
  padding: 4px;
}

.page-tabs button {
  background: transparent;
  border: 0;
  border-radius: 6px;
  color: #475569;
  cursor: pointer;
  font-weight: 750;
  min-height: 36px;
  padding: 0 14px;
}

.page-tabs button.active {
  background: #ffffff;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.14);
  color: #0f172a;
}

.topbar h1,
.section-head h2,
.problem-body h3 {
  color: #111827;
  margin: 0;
}

.topbar h1 {
  font-size: 28px;
  font-weight: 750;
  line-height: 1.2;
}

.eyebrow {
  color: #64748b;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  margin: 0 0 4px;
  text-transform: uppercase;
}

.topbar-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

.topbar-meta span,
.difficulty {
  background: #e0f2fe;
  border: 1px solid #bae6fd;
  border-radius: 999px;
  color: #075985;
  font-size: 13px;
  font-weight: 700;
  padding: 6px 10px;
}

.workspace {
  display: grid;
  gap: 20px;
  grid-template-columns: minmax(320px, 0.8fr) minmax(520px, 1.35fr);
  min-height: 640px;
}

.submissions-section {
  margin-top: 20px;
}

.admin-page {
  display: grid;
  gap: 20px;
  grid-template-columns: minmax(380px, 0.82fr) minmax(520px, 1.18fr);
}

.panel {
  background: #ffffff;
  border: 1px solid #d7dde7;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
  min-width: 0;
  padding: 20px;
}

.problem-panel,
.editor-panel {
  display: flex;
  flex-direction: column;
}

.section-head {
  align-items: flex-start;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.section-head h2 {
  font-size: 20px;
  font-weight: 750;
  line-height: 1.25;
}

.field-label,
.form-field span {
  color: #475569;
  display: block;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 8px;
}

.control {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  color: #111827;
  min-height: 42px;
  outline: none;
  padding: 9px 11px;
  width: 100%;
}

.control:focus {
  border-color: #0284c7;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.14);
}

.problem-select {
  margin-bottom: 18px;
}

.problem-body {
  border-top: 1px solid #e2e8f0;
  color: #334155;
  line-height: 1.75;
  overflow: auto;
  padding-top: 18px;
}

.problem-title-row {
  align-items: center;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.problem-title-row h3 {
  font-size: 22px;
  line-height: 1.3;
}

.problem-title-row span {
  color: #64748b;
  font-weight: 700;
}

.problem-body p {
  margin: 0;
  white-space: pre-wrap;
}

.format-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  display: grid;
  gap: 12px;
  margin-top: 20px;
  padding: 14px;
}

.format-box strong {
  color: #111827;
}

.empty-state,
.empty-row {
  color: #64748b;
  text-align: center;
}

.empty-state {
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  padding: 32px 16px;
}

.editor-toolbar {
  align-items: center;
}

.lang-select {
  max-width: 160px;
}

.editor-container {
  border: 1px solid #111827;
  border-radius: 8px;
  flex: 1;
  min-height: 460px;
  overflow: hidden;
}

.submit-bar {
  align-items: center;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  display: flex;
  gap: 16px;
  justify-content: space-between;
  margin-top: 16px;
  padding: 14px;
}

.submit-btn,
.admin-btn {
  border: 0;
  border-radius: 6px;
  color: #ffffff;
  cursor: pointer;
  font-weight: 750;
  min-height: 42px;
  padding: 0 18px;
}

.submit-btn {
  background: #0284c7;
}

.submit-btn:hover,
.admin-btn:hover {
  filter: brightness(0.95);
}

.submit-btn:disabled,
.admin-btn:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  filter: none;
}

.status-card {
  align-items: center;
  color: #334155;
  display: flex;
  flex-wrap: wrap;
  font-size: 14px;
  gap: 10px;
  justify-content: flex-end;
}

.status-card.muted {
  color: #64748b;
}

.badge {
  background: #e2e8f0;
  border-radius: 999px;
  color: #334155;
  font-weight: 750;
  padding: 5px 10px;
}

.badge-pending {
  background: #fef3c7;
  color: #92400e;
}

.badge-ac {
  background: #dcfce7;
  color: #166534;
}

.badge-error {
  background: #fee2e2;
  color: #991b1b;
}

.admin-form {
  display: grid;
  gap: 14px;
  grid-template-columns: minmax(0, 1fr) 150px;
}

.form-field {
  min-width: 0;
}

.span-all {
  grid-column: 1 / -1;
}

.admin-textarea {
  min-height: 118px;
  resize: vertical;
}

.small-textarea {
  min-height: 72px;
  resize: vertical;
}

.check-field {
  align-items: center;
  color: #334155;
  display: inline-flex;
  font-weight: 700;
  gap: 8px;
}

.check-field input {
  height: 16px;
  width: 16px;
}

.admin-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.admin-btn {
  background: #0f766e;
  justify-self: start;
}

.ghost-btn {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  color: #334155;
  cursor: pointer;
  font-weight: 750;
  min-height: 42px;
  padding: 0 14px;
}

.ghost-btn:hover {
  background: #f8fafc;
}

.admin-message {
  color: #334155;
  font-size: 14px;
  margin: 12px 0 0;
}

.upload-form {
  display: grid;
  gap: 14px;
}

.file-control {
  padding: 8px 10px;
}

.case-list {
  border-top: 1px solid #e2e8f0;
  margin-top: 18px;
  padding-top: 18px;
}

.case-list h3 {
  color: #111827;
  font-size: 16px;
  margin: 0 0 12px;
}

.case-item {
  align-items: center;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  display: grid;
  gap: 8px;
  grid-template-columns: 48px 1fr 1fr;
  margin-bottom: 8px;
  padding: 10px;
}

.case-item span {
  color: #0f172a;
  font-weight: 800;
}

.case-item code {
  background: #f8fafc;
  border-radius: 6px;
  color: #475569;
  font-family: ui-monospace, Consolas, monospace;
  font-size: 12px;
  overflow: hidden;
  padding: 6px 8px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.problem-list {
  display: grid;
  gap: 12px;
}

.problem-item {
  align-items: flex-start;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  display: flex;
  gap: 16px;
  justify-content: space-between;
  padding: 14px;
}

.problem-item h3 {
  color: #111827;
  font-size: 16px;
  line-height: 1.35;
  margin: 0 0 6px;
}

.problem-item p {
  color: #475569;
  display: -webkit-box;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.problem-item small {
  color: #64748b;
  display: block;
  font-weight: 700;
  margin-top: 10px;
}

.problem-item-actions {
  align-items: flex-end;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  gap: 10px;
}

.table-wrap {
  overflow-x: auto;
}

.history-table {
  border-collapse: collapse;
  min-width: 620px;
  width: 100%;
}

.history-table th,
.history-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 13px 12px;
  text-align: left;
  white-space: nowrap;
}

.history-table th {
  background: #f8fafc;
  color: #475569;
  font-size: 13px;
  font-weight: 750;
}

.history-table tbody tr:hover {
  background: #f8fafc;
}

.col-id {
  color: #0f172a;
  font-weight: 750;
}

.col-time {
  color: #64748b;
  font-size: 14px;
}

.lang-pill {
  background: #eef2ff;
  border-radius: 999px;
  color: #3730a3;
  display: inline-flex;
  font-size: 13px;
  font-weight: 700;
  padding: 4px 9px;
}

.status-text {
  font-weight: 800;
}

.is-ac {
  color: #15803d;
}

.is-pending {
  color: #b45309;
}

.is-err {
  color: #b91c1c;
}

@media (max-width: 1100px) {
  .workspace,
  .admin-page {
    grid-template-columns: 1fr;
  }

  .workspace {
    min-height: 0;
  }

  .editor-container {
    min-height: 440px;
  }
}

@media (max-width: 720px) {
  .oj-page {
    padding: 14px;
  }

  .topbar,
  .submit-bar {
    align-items: stretch;
    flex-direction: column;
  }

  .topbar-actions {
    align-items: stretch;
  }

  .page-tabs {
    width: 100%;
  }

  .page-tabs button {
    flex: 1;
  }

  .topbar-meta,
  .status-card {
    justify-content: flex-start;
  }

  .admin-form {
    grid-template-columns: 1fr;
  }

  .admin-btn {
    justify-self: stretch;
  }

  .case-item,
  .problem-item {
    grid-template-columns: 1fr;
  }

  .problem-item {
    flex-direction: column;
  }

  .problem-item-actions {
    align-items: stretch;
    width: 100%;
  }
}
</style>
