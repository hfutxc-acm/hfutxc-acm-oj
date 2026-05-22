<script setup>
import DifficultyBadge from '../problem/DifficultyBadge.vue'
import { navigateTo } from '../../router'

defineProps({
  cid: [String, Number],
  problems: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>编号</th><th>标题</th><th>难度</th><th>通过率</th></tr></thead>
      <tbody>
        <tr v-for="problem in problems" :key="problem.id">
          <td>{{ problem.contestIndex }}</td>
          <td><button class="link-button" @click="navigateTo(`/contests/${cid}/problems/${problem.id}`)">{{ problem.title }}</button></td>
          <td><DifficultyBadge :difficulty="problem.difficulty" /></td>
          <td>{{ problem.passRate || 0 }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
