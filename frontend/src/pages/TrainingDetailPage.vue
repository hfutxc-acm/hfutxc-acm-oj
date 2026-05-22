<script setup>
import { onMounted, ref } from 'vue'
import { getTraining, getTrainingProblems } from '../api/trainings'
import TrainingProgress from '../components/training/TrainingProgress.vue'
import TrainingProblemList from '../components/training/TrainingProblemList.vue'
import { currentRoute } from '../router'

const training = ref(null)
const problems = ref([])

onMounted(async () => {
  training.value = await getTraining(currentRoute.value.params.tid)
  problems.value = await getTrainingProblems(currentRoute.value.params.tid)
})
</script>

<template>
  <section v-if="training" class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">{{ training.type }}</p>
      <h1>{{ training.title }}</h1>
      <p>{{ training.description }}</p>
      <TrainingProgress :done="training.done" :total="training.count" />
    </div>
    <div class="panel">
      <h2>推荐学习顺序</h2>
      <TrainingProblemList :problems="problems" />
    </div>
  </section>
</template>
