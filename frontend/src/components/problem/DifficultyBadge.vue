<script setup>
defineProps({
  difficulty: { type: String, default: '入门' }
})
</script>

<template>
  <span class="badge difficulty-badge">{{ difficulty }}</span>
</template>
