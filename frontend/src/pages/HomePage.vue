<script setup>
import { onMounted, ref } from 'vue'
import { announcements, mockStats, roadmap } from '../api/mock'
import { getContests } from '../api/contests'
import { getRankings } from '../api/rankings'
import { getProblems } from '../api/problems'
import StatCard from '../components/common/StatCard.vue'
import { navigateTo } from '../router'

const stats = ref(mockStats)
const contests = ref([])
const ranks = ref([])

onMounted(async () => {
  const problems = await getProblems()
  contests.value = await getContests()
  ranks.value = await getRankings()
  stats.value = { ...mockStats, problems: problems.length || mockStats.problems }
})
</script>

<template>
  <div class="page-grid">
    <section class="hero-section">
      <p class="eyebrow">HFUTXC ACM Team Portal</p>
      <h1>HFUTXC ACM Online Judge</h1>
      <p>服务校内 ACM 训练、比赛、交流与招新</p>
      <div class="hero-actions">
        <button class="primary-btn" @click="navigateTo('/problems')">开始刷题</button>
        <button class="ghost-btn" @click="navigateTo('/trainings')">新生入门</button>
        <button class="ghost-btn" @click="navigateTo('/contests')">查看比赛</button>
        <button class="ghost-btn" @click="navigateTo('/about/join')">加入 ACM</button>
      </div>
    </section>

    <section class="stat-grid">
      <StatCard label="题目数量" :value="stats.problems" note="校内题库持续沉淀" />
      <StatCard label="用户数量" :value="stats.users" note="训练队与新生" />
      <StatCard label="今日提交" :value="stats.todaySubmissions" note="mock，待接统计接口" />
      <StatCard label="近期比赛" :value="stats.upcomingContests" note="周赛 / 校赛 / 补题" />
    </section>

    <section class="content-grid two-col">
      <div class="panel">
        <div class="section-title-row"><h2>最近比赛</h2><button class="link-button" @click="navigateTo('/contests')">全部比赛</button></div>
        <article v-for="contest in contests" :key="contest.id" class="list-card">
          <div><strong>{{ contest.title }}</strong><p>{{ contest.start }} · {{ contest.status }}</p></div>
          <button class="ghost-btn small" @click="navigateTo(`/contests/${contest.id}`)">进入</button>
        </article>
      </div>

      <div class="panel">
        <div class="section-title-row"><h2>新生训练路线</h2><button class="link-button" @click="navigateTo('/trainings')">开始训练</button></div>
        <ol class="roadmap">
          <li v-for="item in roadmap" :key="item">{{ item }}</li>
        </ol>
      </div>
    </section>

    <section class="content-grid two-col">
      <div class="panel">
        <h2>公告 / 战绩</h2>
        <article v-for="item in announcements" :key="item.title" class="list-card">
          <div><strong>{{ item.title }}</strong><p>{{ item.type }} · {{ item.date }}</p></div>
        </article>
      </div>
      <div class="panel">
        <div class="section-title-row"><h2>活跃榜</h2><button class="link-button" @click="navigateTo('/rankings')">总排名</button></div>
        <article v-for="row in ranks" :key="row.rank" class="rank-card">
          <span>#{{ row.rank }}</span><strong>{{ row.username }}</strong><em>{{ row.ac }} AC</em>
        </article>
      </div>
    </section>
  </div>
</template>
