<script setup>
import VerdictBadge from './VerdictBadge.vue'
import { navigateTo } from '../../router'

defineProps({
  submissions: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th>提交 ID</th>
          <th>用户</th>
          <th>题目</th>
          <th>语言</th>
          <th>状态</th>
          <th>用时</th>
          <th>内存</th>
          <th>提交时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in submissions" :key="item.id">
          <td><button class="link-button" @click="navigateTo(`/submissions/${item.id}`)">#{{ item.id }}</button></td>
          <td>{{ item.user }}</td>
          <td>{{ item.problem_title }}</td>
          <td>{{ item.language }}</td>
          <td><VerdictBadge :status="item.status" /></td>
          <td>{{ item.time_ms }} ms</td>
          <td>{{ item.memory_kb }} KB</td>
          <td>{{ item.created_at }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
