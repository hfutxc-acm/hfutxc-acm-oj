<script setup>
import { currentRoute, navigateTo } from '../../router'
import { authStore } from '../../stores/authStore'

const navItems = [
  { label: '首页', path: '/' },
  { label: '题库', path: '/problems' },
  { label: '训练', path: '/trainings' },
  { label: '比赛', path: '/contests' },
  { label: '提交', path: '/submissions' },
  { label: '排名', path: '/rankings' },
  { label: '后台', path: '/admin' }
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
    <button class="user-chip" @click="navigateTo('/me')">{{ authStore.currentUser.username }}</button>
  </header>
</template>
