<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { getSubmissions } from '../api/submissions'
import SubmissionTable from '../components/submission/SubmissionTable.vue'
import Pagination from '../components/common/Pagination.vue'
import { useAutoAnimate } from '@formkit/auto-animate/vue'

const submissions = ref([])
let pollTimer = null

const FINAL_STATUSES = ['AC', 'WA', 'TLE', 'MLE', 'RE', 'CE', 'SE', 'Accepted', 'Wrong Answer']

const hasPending = computed(() => {
  return submissions.value.some(s => !FINAL_STATUSES.some(fs => s.status.includes(fs)))
})

async function fetchSubmissions() {
  try {
    submissions.value = await getSubmissions()
  } catch (e) {
    console.error('Failed to fetch submissions', e)
  }
}

function startPolling() {
  if (pollTimer) return
  pollTimer = setInterval(async () => {
    await fetchSubmissions()
    if (!hasPending.value) {
      clearInterval(pollTimer)
      pollTimer = null
    }
  }, 2000)
}

onMounted(async () => {
  await fetchSubmissions()
  if (hasPending.value) {
    startPolling()
  }
})

onUnmounted(() => {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Submissions</p>
      <h1>全站提交记录</h1>
      <p>查看最近代码提交和评测状态。<span v-if="hasPending" class="live-dot">● LIVE</span></p>
    </div>
    <SubmissionTable :submissions="submissions" />
    <Pagination :total="submissions.length" />
  </section>
</template>

<style scoped>
.live-dot {
  color: #22c55e;
  font-size: 0.85rem;
  font-weight: 700;
  margin-left: 0.5rem;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>
