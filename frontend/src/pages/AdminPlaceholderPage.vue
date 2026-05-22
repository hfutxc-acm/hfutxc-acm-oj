<script setup>
import { currentRoute } from '../router'
</script>

<template>
  <section class="panel">
    <p class="eyebrow">Admin</p>
    <h1>{{ currentRoute.title }}</h1>
    <p>后台模块入口已建立。比赛、训练、用户管理的真实 CRUD 接口后续接入。</p>
    <div class="table-wrap">
      <table class="data-table">
        <thead><tr><th>模块</th><th>状态</th><th>说明</th></tr></thead>
        <tbody><tr><td>{{ currentRoute.title }}</td><td>TODO</td><td>当前为 UI 占位，避免阻塞主链路。</td></tr></tbody>
      </table>
    </div>
  </section>
</template>
