<script setup>
defineProps({
  status: String
})
</script>

<template>
  <span class="badge contest-status">{{ status }}</span>
</template>
