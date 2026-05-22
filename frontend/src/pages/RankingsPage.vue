<script setup>
import { onMounted, ref } from 'vue'
import { getRankings } from '../api/rankings'
import RankTable from '../components/ranking/RankTable.vue'
import { currentRoute, navigateTo } from '../router'

const rows = ref([])

onMounted(async () => {
  rows.value = await getRankings(currentRoute.value.name === 'freshman-ranking' ? 'freshman' : 'all')
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Ranking</p>
      <h1>{{ currentRoute.name === 'freshman-ranking' ? '新生排名' : '总排名' }}</h1>
      <p>展示 AC 数、提交数和最近活跃时间，班级专业等隐私字段不强制展示。</p>
    </div>
    <div class="tabbar">
      <button :class="{ active: currentRoute.name === 'rankings' }" @click="navigateTo('/rankings')">总排名</button>
      <button :class="{ active: currentRoute.name === 'freshman-ranking' }" @click="navigateTo('/rankings/freshman')">新生榜</button>
    </div>
    <RankTable :rows="rows" />
  </section>
</template>
