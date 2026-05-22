<script setup>
defineProps({
  filters: Object
})

const emit = defineEmits(['update'])

const difficulties = ['全部', '入门', '普及-', '普及+', '提高', '省选']
const tags = ['全部', '语法', 'STL', '模拟', '搜索', 'DP', '图论', '数论', '数据结构']
const statuses = ['全部', '未尝试', '已通过', '尝试过']

function patch(key, value) {
  emit('update', { ...filters, [key]: value })
}
</script>

<template>
  <section class="filter-panel">
    <input
      :value="filters.keyword"
      class="control search-control"
      placeholder="按题号、标题、标签搜索"
      @input="patch('keyword', $event.target.value)"
    />
    <select class="control" :value="filters.difficulty" @change="patch('difficulty', $event.target.value)">
      <option v-for="item in difficulties" :key="item">{{ item }}</option>
    </select>
    <select class="control" :value="filters.tag" @change="patch('tag', $event.target.value)">
      <option v-for="item in tags" :key="item">{{ item }}</option>
    </select>
    <select class="control" :value="filters.status" @change="patch('status', $event.target.value)">
      <option v-for="item in statuses" :key="item">{{ item }}</option>
    </select>
  </section>
</template>
