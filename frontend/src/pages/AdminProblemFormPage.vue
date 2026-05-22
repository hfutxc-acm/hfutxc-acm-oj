<script setup>
import { onMounted, ref } from 'vue'
import { createProblem, updateProblem } from '../api/admin'
import { getProblem } from '../api/problems'
import { currentRoute, navigateTo } from '../router'

const isEdit = currentRoute.value.name === 'admin-problem-edit'
const saving = ref(false)
const message = ref('')
const form = ref({
  title: '',
  difficulty: '入门',
  description: '',
  input_description: '',
  output_description: '',
  time_limit_ms: 1000,
  memory_limit_mb: 256,
  is_public: true
})

async function save() {
  saving.value = true
  message.value = '保存中...'
  try {
    const payload = { ...form.value, title: form.value.title.trim() }
    if (isEdit) {
      await updateProblem(currentRoute.value.params.pid, payload)
      message.value = '题目已保存'
    } else {
      const result = await createProblem(payload)
      message.value = `题目 #${result.id} 已创建`
      navigateTo(`/admin/problems/${result.id}/edit`)
    }
  } catch (error) {
    message.value = error.message
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (isEdit) {
    const problem = await getProblem(currentRoute.value.params.pid)
    form.value = {
      title: problem.title || '',
      difficulty: problem.difficulty || '入门',
      description: problem.description || '',
      input_description: problem.input_description || '',
      output_description: problem.output_description || '',
      time_limit_ms: problem.time_limit_ms || 1000,
      memory_limit_mb: problem.memory_limit_mb || 256,
      is_public: problem.is_public !== false
    }
  }
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Admin / Problem Form</p>
      <h1>{{ isEdit ? '编辑题目' : '新建题目' }}</h1>
      <p>分区维护基本信息、题面、测试数据说明和权限设置。</p>
    </div>
    <form class="problem-form panel" @submit.prevent="save">
      <h2>基本信息</h2>
      <label>标题<input v-model="form.title" class="control" required /></label>
      <label>难度<select v-model="form.difficulty" class="control"><option>入门</option><option>普及-</option><option>普及+</option><option>提高</option><option>省选</option><option>Easy</option><option>Medium</option><option>Hard</option></select></label>
      <label>时间限制 ms<input v-model.number="form.time_limit_ms" class="control" type="number" min="100" /></label>
      <label>内存限制 MB<input v-model.number="form.memory_limit_mb" class="control" type="number" min="16" /></label>
      <label class="span-all">题目描述<textarea v-model="form.description" class="control textarea-lg"></textarea></label>
      <label class="span-all">输入格式<textarea v-model="form.input_description" class="control textarea-sm"></textarea></label>
      <label class="span-all">输出格式<textarea v-model="form.output_description" class="control textarea-sm"></textarea></label>
      <label class="check-row span-all"><input v-model="form.is_public" type="checkbox" /> 公开题目</label>
      <div class="action-row span-all">
        <button class="primary-btn" :disabled="saving">{{ saving ? '保存中...' : '保存' }}</button>
        <button class="ghost-btn" type="button" @click="navigateTo('/admin/problems')">返回列表</button>
        <span v-if="message" class="form-message">{{ message }}</span>
      </div>
    </form>
    <div class="panel">
      <h2>测试数据</h2>
      <p>请到“题目管理”列表页上传 zip。格式：根目录包含 1.in / 1.out、2.in / 2.out。</p>
    </div>
  </section>
</template>
