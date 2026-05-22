<script setup>
const props = defineProps({
  done: { type: Number, default: 0 },
  total: { type: Number, default: 1 }
})
</script>

<template>
  <div class="progress-wrap">
    <div class="progress-bar"><span :style="{ width: `${Math.min(100, Math.round((props.done / props.total) * 100))}%` }"></span></div>
    <small>{{ props.done }} / {{ props.total }}</small>
  </div>
</template>
