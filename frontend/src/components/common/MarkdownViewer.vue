<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'
import markdownItKatex from 'markdown-it-katex'
import 'katex/dist/katex.min.css'

const props = defineProps({
  content: { type: String, default: '' }
})

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typography: true
}).use(markdownItKatex)

const renderedContent = computed(() => {
  if (!props.content) return '暂无内容'
  return md.render(props.content)
})
</script>

<template>
  <div class="markdown-viewer" v-html="renderedContent"></div>
</template>

<style scoped>
.markdown-viewer {
  line-height: 1.6;
}
.markdown-viewer :deep(h1),
.markdown-viewer :deep(h2),
.markdown-viewer :deep(h3),
.markdown-viewer :deep(h4),
.markdown-viewer :deep(h5) {
  margin-top: 1.2em;
  margin-bottom: 0.6em;
  font-weight: 600;
}
.markdown-viewer :deep(p) {
  margin-bottom: 1em;
}
.markdown-viewer :deep(pre) {
  background: var(--surface-hover, #f5f5f5);
  padding: 1rem;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1em;
}
.markdown-viewer :deep(code) {
  font-family: Monaco, Consolas, monospace;
  background: var(--surface-hover, #f5f5f5);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}
.markdown-viewer :deep(pre code) {
  background: transparent;
  padding: 0;
  border-radius: 0;
}
.markdown-viewer :deep(blockquote) {
  border-left: 4px solid var(--primary-color, #4facfe);
  padding-left: 1em;
  margin-left: 0;
  color: var(--text-secondary, #666);
}
.markdown-viewer :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}
.markdown-viewer :deep(th),
.markdown-viewer :deep(td) {
  border: 1px solid var(--border-color, #eee);
  padding: 0.5em;
  text-align: left;
}
</style>
