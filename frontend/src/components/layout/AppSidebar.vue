<script setup>
import { navigateTo } from '../../router'

const items = [
  { label: '后台首页', path: '/admin' },
  { label: '题目管理', path: '/admin/problems' },
  { label: '新建题目', path: '/admin/problems/new' },
  { label: '比赛管理', path: '/admin/contests' },
  { label: '训练管理', path: '/admin/trainings' },
  { label: '用户管理', path: '/admin/users' }
]
</script>

<template>
  <aside class="admin-sidebar">
    <button v-for="item in items" :key="item.path" @click="navigateTo(item.path)">{{ item.label }}</button>
  </aside>
</template>
