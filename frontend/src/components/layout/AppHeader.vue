<script setup>
import { currentRoute, navigateTo } from '../../router'
import { authStore } from '../../stores/authStore'
import { themeStore, toggleTheme } from '../../stores/themeStore'

const navItems = [
  { label: '首页', path: '/' },
  { label: '题库', path: '/problems' },
  { label: '训练', path: '/trainings' },
  { label: '比赛', path: '/contests' },
  { label: '发布题解', path: '/solutions/publish' },
  { label: '排行', path: '/rankings' },
  { label: '团队', path: '/teams' },
  { label: '管理', path: '/admin' },
  { label: '知识库', path: '/wiki', external: true }
]

function handleNavClick(item) {
  if (item.external) {
    window.location.href = item.path
  } else {
    navigateTo(item.path)
  }
}

function isActive(path) {
  if (path === '/') return currentRoute.value.name === 'home'
  return currentRoute.value.name?.startsWith(path.slice(1).split('/')[0])
}
</script>

<template>
  <header class="app-header">
    <button class="brand" @click="navigateTo('/')">
      <strong>HFUTXC ACM</strong>
      <span>Online Judge</span>
    </button>
    <nav class="main-nav">
      <button
        v-for="item in navItems"
        :key="item.path"
        :class="{ active: isActive(item.path) }"
        @click="handleNavClick(item)"
      >
        {{ item.label }}
      </button>
    </nav>
    <div class="header-actions">
      <button class="theme-toggle-btn" @click="toggleTheme" aria-label="Toggle Theme">
        <span v-if="themeStore.currentTheme === 'dark'" class="icon">☀️</span>
        <span v-else class="icon">🌙</span>
      </button>
      <div v-if="authStore.isAuthenticated" class="user-chip-group">
        <button class="user-chip" @click="navigateTo(`/users/${authStore.currentUser.id}`)">{{ authStore.currentUser.username }}</button>
        <button class="btn btn-sm btn-outline" @click="logout">退出</button>
      </div>
      <button v-else class="btn btn-sm btn-primary" @click="navigateTo('/auth')">登录 / 注册</button>
    </div>
  </header>
</template>

<script>
import { logout } from '../../stores/authStore'
export default {
  methods: { logout }
}
</script>

<style scoped>
.user-chip-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
}
</style>
