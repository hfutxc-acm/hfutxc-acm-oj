<script setup>
defineProps({
  rows: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>排名</th><th>用户名</th><th>签名</th><th>AC 数</th><th>提交数</th><th>通过率</th><th>最近活跃</th></tr></thead>
      <tbody>
        <tr v-for="row in rows" :key="row.rank">
          <td>{{ row.rank }}</td>
          <td>{{ row.username }}</td>
          <td>{{ row.signature }}</td>
          <td>{{ row.ac }}</td>
          <td>{{ row.submissions }}</td>
          <td>{{ Math.round((row.ac / row.submissions) * 100) }}%</td>
          <td>{{ row.lastActive }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
