<script setup>
defineProps({
  rows: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
    <table class="data-table contest-rank">
      <thead><tr><th>排名</th><th>用户 / 队伍</th><th>通过题数</th><th>罚时</th><th>题目状态</th></tr></thead>
      <tbody>
        <tr v-for="row in rows" :key="row.rank">
          <td>{{ row.rank }}</td>
          <td>{{ row.team }}</td>
          <td>{{ row.solved }}</td>
          <td>{{ row.penalty }}</td>
          <td class="problem-status-list"><span v-for="(p, i) in row.problems" :key="i">{{ p }}</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
