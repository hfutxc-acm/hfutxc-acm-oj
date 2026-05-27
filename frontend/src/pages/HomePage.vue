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
  <div class="page-grid homepage">
    <section class="hero-section">
      <p class="eyebrow">HFUTXC Online Judge</p>
      <h1>合肥工业大学宣城校区程序设计训练平台</h1>
      <p>面向新手引导、系统训练、比赛交流与梯队建设的现代校园 OJ</p>
      <div class="hero-actions">
        <button class="primary-btn" @click="navigateTo('/problems')">开始刷题</button>
        <button class="ghost-btn" @click="navigateTo('/trainings')">查看训练路线</button>
        <button class="ghost-btn" @click="navigateTo('/about/join')">加入我们</button>
      </div>
    </section>

    <section class="stat-grid">
      <StatCard label="题目数量" :value="stats.problems" note="精选优质题目" />
      <StatCard label="训练题单数" :value="24" note="分阶段系统训练" />
      <StatCard label="比赛场次" :value="12" note="含历年校赛VP" />
      <StatCard label="队伍奖项" :value="48" note="XCPC 累计获奖" />
      <StatCard label="活跃提交数" :value="stats.todaySubmissions" note="今日提交" />
    </section>

    <section class="portal-grid">
      <div class="portal-card new-user">
        <h2>新人入口</h2>
        <p>找不到方向？从这里开始你的算法之旅</p>
        <div class="portal-links">
          <button class="ghost-btn small" @click="navigateTo('/trainings?tag=zero')">我是零基础</button>
          <button class="ghost-btn small" @click="navigateTo('/trainings?tag=cpp')">我会 C++</button>
          <button class="ghost-btn small" @click="navigateTo('/trainings?tag=icpc')">我想打 ICPC</button>
          <button class="ghost-btn small" @click="navigateTo('/contests?tag=freshman')">我想参加校赛</button>
        </div>
      </div>
      
      <div class="portal-card training">
        <h2>训练入口</h2>
        <p>系统化提升，拒绝盲目刷题</p>
        <div class="portal-links">
          <button class="ghost-btn small" @click="navigateTo('/trainings')">本周训练</button>
          <button class="ghost-btn small" @click="navigateTo('/contests')">最近比赛 VP</button>
          <button class="ghost-btn small" @click="navigateTo('/trainings')">专题题单</button>
          <button class="ghost-btn small" @click="navigateTo('/trainings')">校赛真题</button>
        </div>
      </div>
      
      <div class="portal-card propaganda">
        <h2>关于我们</h2>
        <p>了解 HFUTXC ACM 实验室</p>
        <div class="portal-links">
          <button class="ghost-btn small" @click="navigateTo('/about')">实验室介绍</button>
          <button class="ghost-btn small" @click="navigateTo('/about')">获奖记录</button>
          <button class="ghost-btn small" @click="navigateTo('/about')">成员风采</button>
          <button class="ghost-btn small" @click="navigateTo('/about/join')">加入方式</button>
        </div>
      </div>
    </section>

    <section class="content-grid two-col dynamic-area">
      <div class="panel">
        <div class="section-title-row">
          <h2>最近比赛</h2>
          <button class="link-button" @click="navigateTo('/contests')">全部比赛</button>
        </div>
        <article v-for="contest in contests.slice(0, 3)" :key="contest.id" class="list-card">
          <div>
            <strong>{{ contest.title }}</strong>
            <p>{{ contest.start }} · {{ contest.status }}</p>
          </div>
          <button class="ghost-btn small" @click="navigateTo(`/contests/${contest.id}`)">进入</button>
        </article>
      </div>

      <div class="panel">
        <div class="section-title-row">
          <h2>动态与题解</h2>
          <button class="link-button" @click="navigateTo('/solutions')">前往题解区</button>
        </div>
        <article v-for="item in announcements.slice(0, 3)" :key="item.title" class="list-card">
          <div>
            <strong>{{ item.title }}</strong>
            <p>{{ item.type }} · {{ item.date }}</p>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.homepage {
  gap: 2rem;
}
.portal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}
.portal-card {
  background: var(--surface-2);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.portal-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}
.portal-card p {
  color: var(--text-2);
  font-size: 0.9rem;
  margin: 0;
}
.portal-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: auto;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}
</style>
