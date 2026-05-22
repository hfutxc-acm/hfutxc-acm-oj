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
      <DifficultyBadge :difficulty="problem.difficulty" />
    </header>
    <div class="meta-grid">
      <span>时间限制 {{ problem.time_limit_ms || 1000 }} ms</span>
      <span>内存限制 {{ problem.memory_limit_mb || 256 }} MB</span>
      <span>来源 {{ problem.source }}</span>
      <span>通过率 {{ problem.passRate || 0 }}%</span>
    </div>
    <div class="tag-row"><ProblemTag v-for="tag in problem.tags" :key="tag" :tag="tag" /></div>

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
  </article>
</template>
