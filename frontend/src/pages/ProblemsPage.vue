<script setup>
import { computed, onMounted, ref } from 'vue'
import EmptyState from '../components/common/EmptyState.vue'
import Pagination from '../components/common/Pagination.vue'
import ProblemFilter from '../components/problem/ProblemFilter.vue'
import ProblemTable from '../components/problem/ProblemTable.vue'
import { getProblems } from '../api/problems'
import { navigateTo, routeState } from '../router'

const problems = ref([])
const filters = ref({
  keyword: routeState.query.keyword || '',
  stage: routeState.query.stage || '全部',
  difficulty: routeState.query.difficulty || '全部',
  tag: routeState.query.tag || '全部',
  source: routeState.query.source || '全部',
  status: routeState.query.status || '全部',
  searchContent: routeState.query.searchContent === 'true'
})

const filtered = computed(() => {
  const keyword = filters.value.keyword.trim().toLowerCase()
  return problems.value.filter(problem => {
    // If searchContent is true, you could also search problem.content, but for now we search title/tags
    const text = `${problem.id} ${problem.title} ${(problem.tags || []).join(' ')} ${filters.value.searchContent && problem.content ? problem.content : ''}`.toLowerCase()
    const okKeyword = !keyword || text.includes(keyword)
    const okDifficulty = filters.value.difficulty === '全部' || problem.difficulty === filters.value.difficulty
    const okTag = filters.value.tag === '全部' || problem.tags?.includes(filters.value.tag)
    const okSource = filters.value.source === '全部' || problem.source === filters.value.source
    
    // Support stage filtering
    const okStage = filters.value.stage === '全部' || problem.stage === filters.value.stage || !problem.stage

    const statusMap = { '未做': 'NONE', '已 AC': 'AC', '尝试过': 'TRIED', '收藏': 'FAVORITE' }
    const okStatus = filters.value.status === '全部' || problem.status === statusMap[filters.value.status]
    return okKeyword && okDifficulty && okTag && okSource && okStage && okStatus
  })
})

function updateFilters(next) {
  filters.value = next
  const params = new URLSearchParams()
  if (next.keyword) params.set('keyword', next.keyword)
  if (next.stage !== '全部') params.set('stage', next.stage)
  if (next.difficulty !== '全部') params.set('difficulty', next.difficulty)
  if (next.tag !== '全部') params.set('tag', next.tag)
  if (next.source !== '全部') params.set('source', next.source)
  if (next.status !== '全部') params.set('status', next.status)
  if (next.searchContent) params.set('searchContent', 'true')
  navigateTo(`/problems${params.toString() ? `?${params}` : ''}`)
}

onMounted(async () => {
  problems.value = await getProblems()
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Problem Set</p>
      <h1>题库</h1>
      <p>按难度、标签和状态筛选校内训练题目。</p>
    </div>
    <ProblemFilter :filters="filters" :total="filtered.length" @update="updateFilters" />
    <ProblemTable v-if="filtered.length" :problems="filtered" />
    <EmptyState v-else title="没有匹配的题目" description="换一个关键词或筛选条件试试。" />
    <Pagination :total="filtered.length" />
  </section>
</template>
