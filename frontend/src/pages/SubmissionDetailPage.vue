<script setup>
import { onMounted, ref } from 'vue'
import { getSubmission } from '../api/submissions'
import SubmissionDetail from '../components/submission/SubmissionDetail.vue'
import { currentRoute } from '../router'

const submission = ref(null)

onMounted(async () => {
  submission.value = await getSubmission(currentRoute.value.params.sid)
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Submission Status</p>
      <h1>测评结果</h1>
    </div>
    <SubmissionDetail :submission="submission" />
    <div class="panel" v-if="submission && submission.results && submission.results.length > 0">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2>测试点详情</h2>
        <span class="badge" style="background: var(--surface-2); border: 1px solid var(--border-color); color: var(--text-2);">详细输出</span>
      </div>
      <div v-for="(res, index) in submission.results" :key="index" style="background: var(--surface-2); border-radius: 8px; padding: 1rem; border: 1px solid var(--border-color); margin-bottom: 1rem;">
        <p style="margin-bottom: 0.5rem;"><strong>测试点 #{{ index + 1 }}</strong> - <span :style="{ color: res.status === 'AC' ? 'var(--ac-color)' : 'var(--error-color)', fontWeight: 'bold' }">{{ res.status }}</span></p>
        <p v-if="res.message" style="color: var(--text-2); font-size: 0.85rem; font-family: var(--font-mono); white-space: pre-wrap; word-break: break-all;">{{ res.message }}</p>
        <div style="margin-top: 0.5rem; font-size: 0.85rem; color: var(--text-2);">
          耗时: {{ res.time_ms }} ms | 内存: {{ res.memory_kb }} KB
        </div>
      </div>
    </div>
  </section>
</template>
