<script setup>
import { computed, onMounted, ref } from 'vue'
import { getTrainings } from '../api/trainings'
import TrainingCard from '../components/training/TrainingCard.vue'

const trainings = ref([])

onMounted(async () => {
  trainings.value = await getTrainings()
})

const categorizedTrainings = computed(() => {
  const categories = [
    { key: 'novice', label: '新手路线', types: ['新生入门'] },
    { key: 'topic', label: '专题训练', types: ['专题训练'] },
    { key: 'contest', label: '比赛复盘训练', types: ['校赛补题'] },
    { key: 'homework', label: '队内作业', types: ['队内作业'] }
  ]
  
  return categories.map(cat => ({
    ...cat,
    items: trainings.value.filter(t => cat.types.includes(t.type))
  })).filter(cat => cat.items.length > 0)
})
</script>

<template>
  <section class="page-grid training-page">
    <div class="page-heading">
      <p class="eyebrow">Training Center</p>
      <h1>训练中心</h1>
      <p>按阶段、分专题的系统化刷题路线。完成各阶段任务以解锁更多权限与称号。</p>
    </div>
    
    <div v-for="category in categorizedTrainings" :key="category.key" class="training-category">
      <h2>{{ category.label }}</h2>
      <div class="card-grid">
        <TrainingCard v-for="training in category.items" :key="training.id" :training="training" />
      </div>
    </div>
  </section>
</template>

<style scoped>
.training-page {
  gap: 2rem;
}
.training-category h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}
</style>
