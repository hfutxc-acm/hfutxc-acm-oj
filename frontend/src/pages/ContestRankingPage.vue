<script setup>
import { onMounted, ref } from 'vue'
import { getContestRanking } from '../api/contests'
import ContestRankTable from '../components/contest/ContestRankTable.vue'

const rows = ref([])

onMounted(async () => {
  rows.value = await getContestRanking()
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Contest Ranking</p>
      <h1>比赛榜单</h1>
      <p>基础 ACM 榜单，后续可扩展封榜、滚榜和气球颜色。</p>
    </div>
    <ContestRankTable :rows="rows" />
  </section>
</template>
