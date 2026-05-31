<script setup>
import { useAuthStore } from '../stores/authStore'
import { currentRoute } from '../router'
</script>

<template>
  <section class="panel profile-page">
    <p class="eyebrow">User</p>
    <h1>{{ currentRoute.name === 'me' ? useAuthStore().currentUser.username : `用户 #${currentRoute.params.uid}` }}</h1>
    <p>个人主页 MVP：后续展示训练进度、AC 列表、比赛记录和个人签名。</p>
  </section>
</template>
