<script setup>
defineProps({
  page: { type: Number, default: 1 },
  total: { type: Number, default: 0 },
  pageSize: { type: Number, default: 20 }
})
</script>

<template>
  <div class="pagination">
    <button disabled>上一页</button>
    <span>第 {{ page }} 页 · 共 {{ total }} 条</span>
    <button disabled>下一页</button>
  </div>
</template>
