<script setup>
import { onMounted, ref } from 'vue'
import { getTrainings } from '../api/trainings'
import TrainingCard from '../components/training/TrainingCard.vue'

const trainings = ref([])

onMounted(async () => {
  trainings.value = await getTrainings()
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Training</p>
      <h1>训练</h1>
      <p>面向新生入门、校赛补题、专题训练和队内作业。</p>
    </div>
    <div class="card-grid">
      <TrainingCard v-for="training in trainings" :key="training.id" :training="training" />
    </div>
  </section>
</template>
