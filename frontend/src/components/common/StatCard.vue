<script setup>
defineProps({
  label: String,
  value: [String, Number],
  note: String
})
</script>

<template>
  <article class="stat-card">
    <span>{{ label }}</span>
    <strong>{{ value }}</strong>
    <small v-if="note">{{ note }}</small>
  </article>
</template>
