<script setup>
const props = defineProps({
  filters: Object
})

const emit = defineEmits(['update'])

const difficulties = ['全部', '入门', '普及-', '普及', '提高', '省选', 'ICPC区域赛']
const tags = ['全部', 'DP', '图论', '数论', '字符串', '数据结构', '计算几何', '语法', 'STL', '模拟', '搜索']
const sources = ['全部', '校赛', '新生赛', 'ICPC', 'CF', '洛谷', '自建']
const stages = ['全部', '大一上', '大一下', '暑训前', '区域赛队员', '校赛备赛']
const statuses = ['全部', '未做', '已 AC', '尝试过', '收藏']

function patch(key, value) {
  emit('update', { ...props.filters, [key]: value })
}
</script>

<template>
  <section class="filter-panel complex-filter">
    <div class="filter-row search-row">
      <input
        :value="filters.keyword"
        class="control search-control"
        placeholder="搜索题目（标题、题号）"
        @input="patch('keyword', $event.target.value)"
      />
    </div>
    <div class="filter-row">
      <label>推荐阶段：</label>
      <select class="control" :value="filters.stage" @change="patch('stage', $event.target.value)">
        <option v-for="item in stages" :key="item">{{ item }}</option>
      </select>

      <label>难度：</label>
      <select class="control" :value="filters.difficulty" @change="patch('difficulty', $event.target.value)">
        <option v-for="item in difficulties" :key="item">{{ item }}</option>
      </select>

      <label>算法：</label>
      <select class="control" :value="filters.tag" @change="patch('tag', $event.target.value)">
        <option v-for="item in tags" :key="item">{{ item }}</option>
      </select>

      <label>来源：</label>
      <select class="control" :value="filters.source" @change="patch('source', $event.target.value)">
        <option v-for="item in sources" :key="item">{{ item }}</option>
      </select>

      <label>状态：</label>
      <select class="control" :value="filters.status" @change="patch('status', $event.target.value)">
        <option v-for="item in statuses" :key="item">{{ item }}</option>
      </select>
    </div>
  </section>
</template>

<style scoped>
.complex-filter {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.filter-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
}
.filter-row label {
  font-size: 0.9rem;
  color: var(--text-2);
  margin-left: 0.5rem;
}
.filter-row label:first-child {
  margin-left: 0;
}
.search-row .search-control {
  max-width: 400px;
  width: 100%;
}
</style>
