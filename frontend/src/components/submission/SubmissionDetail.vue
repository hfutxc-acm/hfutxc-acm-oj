<script setup>
import VerdictBadge from './VerdictBadge.vue'

defineProps({
  submission: Object
})
</script>

<template>
  <section v-if="submission" class="panel">
    <div class="section-title-row">
      <h2>提交 #{{ submission.id }}</h2>
      <VerdictBadge :status="submission.status" />
    </div>
    <div class="detail-grid">
      <span>用户：{{ submission.user }}</span>
      <span>题目：{{ submission.problem_title }}</span>
      <span>语言：{{ submission.language }}</span>
      <span>时间：{{ submission.created_at }}</span>
    </div>
    <pre class="code-preview">// 后端暂未返回源码详情，后续接入 submission detail API。</pre>
  </section>
</template>
