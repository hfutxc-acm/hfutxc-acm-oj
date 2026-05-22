<script setup>
defineProps({
  content: { type: String, default: '' }
})
</script>

<template>
  <div class="markdown-viewer">
    <p v-for="(line, index) in (content || '暂无内容').split('\n')" :key="index">{{ line || ' ' }}</p>
  </div>
</template>
