<script setup>
import { ref } from 'vue'
import { useAutoAnimate } from '@formkit/auto-animate/vue'
import VerdictBadge from './VerdictBadge.vue'
import { navigateTo } from '../../router'

defineProps({
  submissions: { type: Array, default: () => [] }
})

const [tableBody] = useAutoAnimate()
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th>提交 ID</th>
          <th>用户</th>
          <th>题目</th>
          <th>语言</th>
          <th>状态</th>
          <th>用时</th>
          <th>内存</th>
          <th>提交时间</th>
        </tr>
      </thead>
      <tbody ref="tableBody">
        <tr v-if="submissions.length === 0">
          <td colspan="8" style="text-align: center; color: var(--text-3); padding: 2rem;">暂无提交记录</td>
        </tr>
        <tr v-else v-for="item in submissions" :key="item.id" class="submission-row" :class="{ pending: item.status === 'Pending' }">
          <td><button class="link-button" @click="navigateTo(`/submissions/${item.id}`)">#{{ item.id }}</button></td>
          <td>
            <button class="link-button" @click="navigateTo(`/users/${item.user_id}`)">{{ item.user }}</button>
          </td>
          <td>
            <button class="link-button" @click="navigateTo(`/problems/${item.problem_id}`)">{{ item.problem_title }}</button>
          </td>
          <td><span class="lang-tag">{{ item.language }}</span></td>
          <td><VerdictBadge :status="item.status" /></td>
          <td class="mono">{{ item.time_ms }} ms</td>
          <td class="mono">{{ item.memory_kb }} KB</td>
          <td class="time-cell">{{ formatTime(item.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  methods: {
    formatTime(t) {
      if (!t) return '-'
      try {
        const d = new Date(t)
        if (isNaN(d.getTime())) return t
        return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' })
      } catch {
        return t
      }
    }
  }
}
</script>

<style scoped>
.mono {
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 0.85rem;
}

.lang-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.78rem;
  font-weight: 600;
  background: var(--surface-2);
  border: 1px solid var(--border-color);
  color: var(--text-2);
}

.submission-row.pending {
  animation: pendingPulse 2s ease-in-out infinite;
}

@keyframes pendingPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.time-cell {
  font-size: 0.82rem;
  color: var(--text-2);
  white-space: nowrap;
}
</style>
