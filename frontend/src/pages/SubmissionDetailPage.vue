<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { getSubmission } from '../api/submissions'
import SubmissionDetail from '../components/submission/SubmissionDetail.vue'
import VerdictBadge from '../components/submission/VerdictBadge.vue'
import { currentRoute, navigateTo } from '../router'

const submission = ref(null)
const loading = ref(true)
let pollTimer = null

const FINAL_STATUSES = ['AC', 'WA', 'TLE', 'MLE', 'RE', 'CE', 'SE', 'Accepted', 'Wrong Answer']

const isFinal = computed(() => {
  if (!submission.value) return false
  return FINAL_STATUSES.some(s => submission.value.status.includes(s))
})

async function fetchSubmission() {
  try {
    submission.value = await getSubmission(currentRoute.value.params.sid)
  } catch (e) {
    console.error('Failed to fetch submission', e)
  } finally {
    loading.value = false
  }
}

function startPolling() {
  pollTimer = setInterval(async () => {
    await fetchSubmission()
    if (isFinal.value) {
      clearInterval(pollTimer)
      pollTimer = null
    }
  }, 2000)
}

onMounted(async () => {
  await fetchSubmission()
  if (!isFinal.value) {
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
      <p class="eyebrow">Submission #{{ currentRoute.params.sid }}</p>
      <h1>测评结果</h1>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="panel" style="text-align: center; padding: 3rem;">
      <div class="pulse-dot"></div>
      <p style="margin-top: 1rem; color: var(--text-2);">正在加载评测数据...</p>
    </div>

    <template v-else-if="submission">
      <!-- Status Overview Card -->
      <div class="panel judge-overview">
        <div class="judge-status-row">
          <div class="judge-verdict">
            <VerdictBadge :status="submission.status" style="font-size: 1.5rem; padding: 0.5rem 1.2rem;" />
            <div v-if="!isFinal" class="judging-indicator">
              <span class="spin-icon">⏳</span> 评测中...
            </div>
          </div>
          <div class="judge-meta">
            <div class="meta-item">
              <span class="meta-label">题目</span>
              <button class="link-button" @click="navigateTo(`/problems/${submission.problem_id}`)">
                #{{ submission.problem_id }} {{ submission.problem_title }}
              </button>
            </div>
            <div class="meta-item">
              <span class="meta-label">用户</span>
              <button class="link-button" @click="navigateTo(`/users/${submission.user_id}`)">
                {{ submission.user }}
              </button>
            </div>
            <div class="meta-item">
              <span class="meta-label">语言</span>
              <span>{{ submission.language }}</span>
            </div>
            <div class="meta-item" v-if="isFinal">
              <span class="meta-label">用时</span>
              <span class="mono">{{ submission.time_ms }} ms</span>
            </div>
            <div class="meta-item" v-if="isFinal">
              <span class="meta-label">内存</span>
              <span class="mono">{{ submission.memory_kb }} KB</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">提交时间</span>
              <span>{{ submission.created_at }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Test Case Results -->
      <div class="panel" v-if="submission.results && submission.results.length > 0">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h2>测试点详情</h2>
          <span class="badge" style="background: var(--surface-2); border: 1px solid var(--border-color); color: var(--text-2);">
            {{ submission.results.length }} 个测试点
          </span>
        </div>
        <div class="testcase-grid">
          <div v-for="(res, index) in submission.results" :key="index" class="testcase-card" :class="res.status.toLowerCase()">
            <div class="tc-header">
              <strong>#{{ index + 1 }}</strong>
              <VerdictBadge :status="res.status" />
            </div>
            <div class="tc-stats">
              <span>⏱ {{ res.time_ms }} ms</span>
              <span>💾 {{ res.memory_kb }} KB</span>
            </div>
            <p v-if="res.message" class="tc-message">{{ res.message }}</p>
          </div>
        </div>
      </div>

      <!-- Pending animation when no results yet -->
      <div v-else-if="!isFinal" class="panel" style="text-align: center; padding: 2rem;">
        <div class="pulse-dot"></div>
        <p style="margin-top: 1rem; color: var(--text-2);">正在等待评测结果...</p>
      </div>

      <!-- Source Code -->
      <SubmissionDetail :submission="submission" />
    </template>
  </section>
</template>

<style scoped>
.judge-overview {
  background: var(--surface-1);
}

.judge-status-row {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
}

.judge-verdict {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  min-width: 120px;
}

.judging-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--warning-color, #f59e0b);
  animation: pulse 1.5s ease-in-out infinite;
}

.spin-icon {
  display: inline-block;
  animation: spin 1.5s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.pulse-dot {
  width: 16px;
  height: 16px;
  background: var(--primary);
  border-radius: 50%;
  margin: 0 auto;
  animation: pulse 1.2s ease-in-out infinite;
}

.judge-meta {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
  flex: 1;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.meta-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-3, var(--muted));
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-weight: 600;
}

.testcase-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
}

.testcase-card {
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.75rem;
  transition: border-color 0.2s, transform 0.15s;
}

.testcase-card:hover {
  transform: translateY(-1px);
}

.testcase-card.ac {
  border-left: 3px solid var(--ac-color, #22c55e);
}

.testcase-card.wa {
  border-left: 3px solid var(--error-color, #ef4444);
}

.testcase-card.tle {
  border-left: 3px solid #f59e0b;
}

.testcase-card.re, .testcase-card.se, .testcase-card.ce {
  border-left: 3px solid #a855f7;
}

.tc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.tc-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: var(--text-2);
  font-family: ui-monospace, monospace;
}

.tc-message {
  margin-top: 0.5rem;
  font-size: 0.78rem;
  color: var(--text-2);
  font-family: ui-monospace, monospace;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 80px;
  overflow: auto;
}

@media (max-width: 640px) {
  .judge-status-row {
    flex-direction: column;
  }
  .judge-meta {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
