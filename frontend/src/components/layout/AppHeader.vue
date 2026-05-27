<script setup>
import { currentRoute, navigateTo } from '../../router'
import { authStore } from '../../stores/authStore'
import { themeStore, toggleTheme } from '../../stores/themeStore'

const navItems = [
  { label: '首页', path: '/' },
  { label: '题库', path: '/problems' },
  { label: '训练', path: '/trainings' },
  { label: '比赛', path: '/contests' },
  { label: '题解', path: '/solutions' },
  { label: '排行', path: '/rankings' },
  { label: '团队', path: '/teams' },
  { label: '管理', path: '/admin' }
]

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
        @click="navigateTo(item.path)"
      >
        {{ item.label }}
      </button>
    </nav>
    <div class="header-actions">
      <button class="theme-toggle-btn" @click="toggleTheme" aria-label="Toggle Theme">
        <span v-if="themeStore.currentTheme === 'dark'" class="icon">☀️</span>
        <span v-else class="icon">🌙</span>
      </button>
      <button class="user-chip" @click="navigateTo('/me')">{{ authStore.currentUser.username }}</button>
    </div>
  </header>
</template>
