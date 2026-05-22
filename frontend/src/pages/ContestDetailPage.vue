<script setup>
import { onMounted, ref } from 'vue'
import { getContest, getContestProblems } from '../api/contests'
import ContestProblemList from '../components/contest/ContestProblemList.vue'
import { currentRoute, navigateTo } from '../router'

const contest = ref(null)
const problems = ref([])

onMounted(async () => {
  contest.value = await getContest(currentRoute.value.params.cid)
  problems.value = await getContestProblems(currentRoute.value.params.cid)
})
</script>

<template>
  <section v-if="contest" class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">{{ contest.rule }} Contest</p>
      <h1>{{ contest.title }}</h1>
      <p>{{ contest.start }} - {{ contest.end }} · {{ contest.status }}</p>
    </div>
    <div class="tabbar">
      <button class="active">概览</button>
      <button @click="navigateTo(`/contests/${contest.id}/ranking`)">榜单</button>
      <button @click="navigateTo(`/contests/${contest.id}/submissions`)">提交</button>
    </div>
    <div class="panel">
      <h2>比赛说明</h2>
      <p>请遵守校内训练规范，比赛期间独立思考，赛后及时补题。</p>
    </div>
    <div class="panel">
      <h2>题目入口</h2>
      <ContestProblemList :cid="contest.id" :problems="problems" />
    </div>
  </section>
</template>
