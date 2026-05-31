<script setup>
import { onMounted, ref } from 'vue'
import { getProblem } from '../api/problems'
import ProblemStatement from '../components/problem/ProblemStatement.vue'
import SubmitCodePanel from '../components/problem/SubmitCodePanel.vue'
import SubmissionTable from '../components/submission/SubmissionTable.vue'
import EmptyState from '../components/common/EmptyState.vue'
import DifficultyBadge from '../components/problem/DifficultyBadge.vue'
import { getSubmissions } from '../api/submissions'
import { currentRoute, navigateTo } from '../router'

const problem = ref(null)
const submissions = ref([])
const activeTab = ref('statement')

onMounted(async () => {
  problem.value = await getProblem(currentRoute.value.params.pid)
  submissions.value = await getSubmissions()
})

const onSubmitted = async () => {
  activeTab.value = 'submissions'
  submissions.value = await getSubmissions()
}
</script>

<template>
  <section class="page-grid">
    <div class="tabbar">
      <button :class="{ active: activeTab === 'statement' }" @click="activeTab = 'statement'">题面与提交</button>
      <button :class="{ active: activeTab === 'submissions' }" @click="activeTab = 'submissions'">我的提交</button>
      <button @click="navigateTo(`/problems/${currentRoute.params.pid}/solutions`)">查看题解</button>
      <button @click="navigateTo(`/problems/${currentRoute.params.pid}/discussions`)">讨论区</button>
    </div>

    <div v-if="activeTab === 'statement' && problem" class="problem-detail-grid">
      <!-- Left: Reading Area -->
      <div class="reading-area panel">
        <ProblemStatement :problem="problem" />
      </div>

      <!-- Right: Action & Submit Area -->
      <div class="action-area">
        <div class="meta-panel panel" style="margin-bottom: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <DifficultyBadge :difficulty="problem.difficulty" />
            <span style="font-size: 0.9rem; color: var(--text-2);">通过率: {{ problem.passRate || 0 }}%</span>
          </div>
          <div class="limits" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.85rem; color: var(--text-2); margin-bottom: 1rem; padding: 0.8rem; background: var(--surface-2); border-radius: 6px;">
            <div>时间限制: <strong style="color: var(--text-1);">{{ problem.time_limit_ms || 1000 }} ms</strong></div>
            <div>内存限制: <strong style="color: var(--text-1);">{{ problem.memory_limit_mb || 256 }} MB</strong></div>
          </div>
          <div class="actions" style="display: flex; gap: 0.5rem;">
            <button class="ghost-btn" style="flex: 1;" @click="navigateTo(`/trainings`)">加入题单</button>
            <button class="ghost-btn" style="flex: 1;" @click="navigateTo(`/problems/${problem.id}/solutions`)">查看题解</button>
          </div>
        </div>
        <SubmitCodePanel :problem-id="currentRoute.params.pid" @submitted="onSubmitted" />
      </div>
    </div>
    <SubmissionTable v-else-if="activeTab === 'submissions'" :submissions="submissions.filter(item => String(item.problem_id) === String(currentRoute.params.pid))" />
    <EmptyState v-else-if="!problem" title="加载中..." />
    <EmptyState v-else title="暂未开放" description="模块正在建设中。" />
  </section>
</template>
