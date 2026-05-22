<script setup>
import { onMounted, ref } from 'vue'
import { getProblems } from '../api/problems'
import { getTestcases, uploadProblemData } from '../api/admin'
import DifficultyBadge from '../components/problem/DifficultyBadge.vue'
import { navigateTo } from '../router'

const problems = ref([])
const selectedProblemId = ref('')
const selectedFile = ref(null)
const testcases = ref([])
const message = ref('')
const uploading = ref(false)

async function refreshProblems() {
  problems.value = await getProblems()
  if (!selectedProblemId.value && problems.value.length) selectedProblemId.value = problems.value[0].id
}

async function loadTestcases() {
  testcases.value = []
  if (!selectedProblemId.value) return
  try {
    testcases.value = await getTestcases(selectedProblemId.value)
  } catch (error) {
    message.value = error.message
  }
}

async function uploadZip() {
  if (!selectedProblemId.value || !selectedFile.value) {
    message.value = '请选择题目和 zip 文件'
    return
  }
  uploading.value = true
  message.value = '上传中...'
  try {
    const result = await uploadProblemData(selectedProblemId.value, selectedFile.value)
    message.value = `上传成功：${result.case_count} 个测试点`
    selectedFile.value = null
    await refreshProblems()
    await loadTestcases()
  } catch (error) {
    message.value = error.message
  } finally {
    uploading.value = false
  }
}

onMounted(async () => {
  await refreshProblems()
  await loadTestcases()
})
</script>

<template>
  <section class="page-grid">
    <div class="section-title-row">
      <div>
        <p class="eyebrow">Admin / Problems</p>
        <h1>题目管理</h1>
      </div>
      <button class="primary-btn" @click="navigateTo('/admin/problems/new')">新建题目</button>
    </div>

    <div class="panel">
      <h2>测试数据上传</h2>
      <p class="hint">zip 根目录必须包含 1.in / 1.out、2.in / 2.out，不支持子目录。</p>
      <div class="admin-upload-row">
        <select v-model="selectedProblemId" class="control" @change="loadTestcases">
          <option v-for="problem in problems" :key="problem.id" :value="problem.id">#{{ problem.id }} {{ problem.title }}</option>
        </select>
        <input class="control" type="file" accept=".zip" @change="selectedFile = $event.target.files?.[0] || null" />
        <button class="primary-btn" :disabled="uploading" @click="uploadZip">{{ uploading ? '上传中...' : '上传 zip' }}</button>
      </div>
      <p v-if="message" class="form-message">{{ message }}</p>
      <div class="case-list">
        <span v-for="item in testcases" :key="item.id" class="case-pill">#{{ item.sort_order }} {{ item.input_path }}</span>
      </div>
    </div>

    <div class="table-wrap">
      <table class="data-table">
        <thead><tr><th>题号</th><th>标题</th><th>难度</th><th>标签</th><th>公开</th><th>测试数据</th><th>创建者</th><th>更新时间</th><th>操作</th></tr></thead>
        <tbody>
          <tr v-for="problem in problems" :key="problem.id">
            <td>#{{ problem.id }}</td>
            <td>{{ problem.title }}</td>
            <td><DifficultyBadge :difficulty="problem.difficulty" /></td>
            <td class="tag-cell"><span v-for="tag in problem.tags" :key="tag" class="tag">{{ tag }}</span></td>
            <td>{{ problem.is_public === false ? '否' : '是' }}</td>
            <td>{{ problem.testcase_count || 0 }} 个</td>
            <td>admin</td>
            <td>{{ problem.updated_at || '-' }}</td>
            <td class="action-cell">
              <button class="ghost-btn small" @click="navigateTo(`/problems/${problem.id}`)">预览</button>
              <button class="primary-btn small" @click="navigateTo(`/admin/problems/${problem.id}/edit`)">编辑</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
