<script setup>
import { onMounted, ref } from 'vue'
import { getProblem } from '../api/problems'
import ProblemStatement from '../components/problem/ProblemStatement.vue'
import SubmitCodePanel from '../components/problem/SubmitCodePanel.vue'
import SubmissionTable from '../components/submission/SubmissionTable.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { getSubmissions } from '../api/submissions'
import { currentRoute, navigateTo } from '../router'

const problem = ref(null)
const submissions = ref([])
const activeTab = ref('statement')

onMounted(async () => {
  problem.value = await getProblem(currentRoute.value.params.pid)
  submissions.value = await getSubmissions()
})
</script>

<template>
  <section class="page-grid">
    <div class="tabbar">
      <button :class="{ active: activeTab === 'statement' }" @click="activeTab = 'statement'">题面</button>
      <button :class="{ active: activeTab === 'submissions' }" @click="activeTab = 'submissions'">提交记录</button>
      <button @click="navigateTo(`/problems/${currentRoute.params.pid}/solutions`)">题解</button>
      <button @click="navigateTo(`/problems/${currentRoute.params.pid}/discussions`)">讨论</button>
      <button :class="{ active: activeTab === 'stats' }" @click="activeTab = 'stats'">统计</button>
    </div>

    <div v-if="activeTab === 'statement'" class="problem-detail-grid">
      <ProblemStatement :problem="problem" />
      <SubmitCodePanel :problem-id="currentRoute.params.pid" @submitted="activeTab = 'submissions'" />
    </div>
    <SubmissionTable v-else-if="activeTab === 'submissions'" :submissions="submissions.filter(item => String(item.problem_id) === String(currentRoute.params.pid))" />
    <div v-else-if="activeTab === 'stats'" class="panel">
      <h2>统计</h2>
      <p>通过数：{{ problem?.accepted || 0 }}，提交数：{{ problem?.submissions || 0 }}，通过率：{{ problem?.passRate || 0 }}%。</p>
    </div>
    <EmptyState v-else title="暂未开放" description="题解和讨论模块后续接入。" />
  </section>
</template>
