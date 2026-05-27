<script setup>
import TrainingProgress from './TrainingProgress.vue'
import { navigateTo } from '../../router'

defineProps({
  training: Object
})
</script>

<template>
  <article class="training-card">
    <span class="badge">{{ training.type }}</span>
    <h3>{{ training.title }}</h3>
    <p>{{ training.description }}</p>
    <div class="training-meta" v-if="training.prerequisites || training.estimatedTime">
      <div v-if="training.prerequisites" class="meta-item">
        <strong>前置知识:</strong> {{ training.prerequisites }}
      </div>
      <div v-if="training.estimatedTime" class="meta-item">
        <strong>预计耗时:</strong> {{ training.estimatedTime }}
      </div>
    </div>
    <TrainingProgress :done="training.done" :total="training.count" />
    <div class="tag-row"><span v-for="tag in training.tags" :key="tag" class="tag">{{ tag }}</span></div>
    <button class="primary-btn" @click="navigateTo(`/trainings/${training.id}`)">进入训练</button>
  </article>
</template>

<style scoped>
.training-meta {
  margin: 0.5rem 0;
  font-size: 0.85rem;
  color: var(--text-2);
}
.meta-item {
  margin-bottom: 0.2rem;
}
.meta-item strong {
  color: var(--text-1);
}
</style>
