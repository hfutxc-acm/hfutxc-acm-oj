<script setup>
import ContestStatusBadge from './ContestStatusBadge.vue'
import { navigateTo } from '../../router'

defineProps({
  contests: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>比赛名称</th><th>开始时间</th><th>结束时间</th><th>时长</th><th>状态</th><th>赛制</th><th>操作</th></tr></thead>
      <tbody>
        <tr v-for="contest in contests" :key="contest.id">
          <td>{{ contest.title }}</td>
          <td>{{ contest.start }}</td>
          <td>{{ contest.end }}</td>
          <td>{{ contest.duration }}</td>
          <td><ContestStatusBadge :status="contest.status" /></td>
          <td>{{ contest.rule }}</td>
          <td class="action-cell">
            <button class="primary-btn small" @click="navigateTo(`/contests/${contest.id}`)">进入</button>
            <button class="ghost-btn small" @click="navigateTo(`/contests/${contest.id}/ranking`)">榜单</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
