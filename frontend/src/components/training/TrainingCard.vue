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
    <TrainingProgress :done="training.done" :total="training.count" />
    <div class="tag-row"><span v-for="tag in training.tags" :key="tag" class="tag">{{ tag }}</span></div>
    <button class="primary-btn" @click="navigateTo(`/trainings/${training.id}`)">进入训练</button>
  </article>
</template>
