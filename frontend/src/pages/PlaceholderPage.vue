<script setup>
import { currentRoute, navigateTo } from '../router'
</script>

<template>
  <section class="panel placeholder-page">
    <p class="eyebrow">Coming Soon</p>
    <h1>{{ currentRoute.title }}</h1>
    <p>这个入口已预留，MVP 阶段先展示占位页，后续可以接入完整功能。</p>
    <button class="primary-btn" @click="navigateTo('/')">返回首页</button>
  </section>
</template>
