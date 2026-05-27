<script setup>
import MarkdownViewer from '../common/MarkdownViewer.vue'
import DifficultyBadge from './DifficultyBadge.vue'
import ProblemTag from './ProblemTag.vue'

defineProps({
  problem: Object
})
</script>

<template>
  <article v-if="problem" class="statement">
    <header class="statement-head">
      <div>
        <p class="eyebrow">Problem #{{ problem.id }}</p>
        <h1>{{ problem.title }}</h1>
      </div>
    </header>

    <section class="statement-block">
      <h2>题目描述</h2>
      <MarkdownViewer :content="problem.description" />
    </section>
    <section class="statement-block">
      <h2>输入格式</h2>
      <MarkdownViewer :content="problem.input_description" />
    </section>
    <section class="statement-block">
      <h2>输出格式</h2>
      <MarkdownViewer :content="problem.output_description" />
    </section>
    <section class="sample-grid">
      <div>
        <h2>样例输入</h2>
        <pre>{{ problem.sample_input || '暂无样例' }}</pre>
      </div>
      <div>
        <h2>样例输出</h2>
        <pre>{{ problem.sample_output || '暂无样例' }}</pre>
      </div>
    </section>
    
    <section class="statement-block source-tags" style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
      <p style="color: var(--text-2); font-size: 0.9rem; margin-bottom: 0.5rem;">来源：{{ problem.source }}</p>
      <div class="tag-row"><ProblemTag v-for="tag in problem.tags" :key="tag" :tag="tag" /></div>
    </section>
  </article>
</template>
