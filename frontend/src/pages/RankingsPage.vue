<script setup>
import { onMounted, ref, watch } from 'vue'
import { getRankings } from '../api/rankings'
import RankTable from '../components/ranking/RankTable.vue'
import { currentRoute, navigateTo, routeState } from '../router'

const rows = ref([])

const tabs = [
  { id: 'all', label: '总榜' },
  { id: 'active', label: '本周活跃榜' },
  { id: 'freshman', label: '新生榜' },
  { id: 'topic', label: '专题完成榜' },
  { id: 'solution', label: '题解贡献榜' }
]

const currentTab = ref(routeState.query.tab || 'all')

watch(() => routeState.query.tab, async (newTab) => {
  currentTab.value = newTab || 'all'
  rows.value = await getRankings(currentTab.value)
})

onMounted(async () => {
  rows.value = await getRankings(currentTab.value)
})

function changeTab(tabId) {
  navigateTo(`/rankings?tab=${tabId}`)
}
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Leaderboards</p>
      <h1>排行榜</h1>
      <p>多维度的荣誉榜单，让每个人都有被看见的机会。</p>
    </div>
    <div class="tabbar">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        :class="{ active: currentTab === tab.id }" 
        @click="changeTab(tab.id)"
      >
        {{ tab.label }}
      </button>
    </div>
    <RankTable :rows="rows" />
  </section>
</template>
