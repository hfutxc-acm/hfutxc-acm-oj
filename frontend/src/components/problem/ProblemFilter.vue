<script setup>
import { computed } from 'vue'

const props = defineProps({
  filters: Object,
  total: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['update'])

const difficulties = ['全部', '入门', '普及-', '普及', '提高', '省选', 'ICPC区域赛']
const tags = ['全部', 'DP', '图论', '数论', '字符串', '数据结构', '计算几何', '语法', 'STL', '模拟', '搜索']
const sources = ['全部', '洛谷', 'Codeforces', 'SPOJ', '校赛', '新生赛', 'ICPC', '自建']
const statuses = ['全部', '未做', '已 AC', '尝试过', '收藏']

function patch(key, value) {
  emit('update', { ...props.filters, [key]: value })
}

function clearFilters() {
  emit('update', {
    ...props.filters,
    keyword: '',
    difficulty: '全部',
    tag: '全部',
    status: '全部',
    searchContent: false
  })
}

const activeFiltersText = computed(() => {
  const parts = []
  if (props.filters.difficulty !== '全部') parts.push(props.filters.difficulty)
  if (props.filters.tag !== '全部') parts.push(props.filters.tag)
  if (props.filters.status !== '全部') parts.push(props.filters.status)
  if (props.filters.searchContent) parts.push('搜索题面')
  if (props.filters.keyword) parts.push(`"${props.filters.keyword}"`)
  return parts.length ? parts.join(', ') : '暂无'
})
</script>

<template>
  <section class="filter-panel complex-filter" style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;">
    <!-- Row 1: 所属题库 -->
    <div class="filter-row">
      <span class="row-label">所属题库：</span>
      <div class="tab-list">
        <button 
          v-for="src in sources" 
          :key="src"
          class="tab-item"
          :class="{ active: filters.source === src }"
          @click="patch('source', src)"
        >
          {{ src }}
        </button>
      </div>
    </div>

    <!-- Row 2: 筛选条件 & 关键词 -->
    <div class="filter-row">
      <span class="row-label">筛选条件：</span>
      <select class="control select-control" :value="filters.difficulty" @change="patch('difficulty', $event.target.value)">
        <option value="全部">题目难度</option>
        <option v-for="item in difficulties.slice(1)" :key="item" :value="item">{{ item }}</option>
      </select>
      <select class="control select-control" :value="filters.tag" @change="patch('tag', $event.target.value)">
        <option value="全部">算法/来源</option>
        <option v-for="item in tags.slice(1)" :key="item" :value="item">{{ item }}</option>
      </select>
      <select class="control select-control" :value="filters.status" @change="patch('status', $event.target.value)">
        <option value="全部">状态</option>
        <option v-for="item in statuses.slice(1)" :key="item" :value="item">{{ item }}</option>
      </select>
      
      <span class="row-label" style="margin-left: 8px;">关键词：</span>
      <input
        :value="filters.keyword"
        class="control search-input"
        placeholder="算法、标题或题目编号"
        @input="patch('keyword', $event.target.value)"
        @keyup.enter="patch('keyword', filters.keyword)"
      />
      <label class="checkbox-label">
        <input type="checkbox" :checked="filters.searchContent" @change="patch('searchContent', $event.target.checked)" />
        搜索题面
      </label>
    </div>

    <!-- Row 3: 已选择 & 查看帮助 -->
    <div class="filter-row status-row">
      <span class="status-text">已选择：<span class="status-val">{{ activeFiltersText }}</span></span>
      <a href="#" class="help-link">查看帮助</a>
    </div>

    <!-- Row 4: 统计与操作 -->
    <div class="filter-row action-row">
      <span class="total-text">共计 {{ total }} 条结果</span>
      <div class="actions">
        <a href="#" class="clear-btn" @click.prevent="clearFilters">清除筛选</a>
        <button class="search-btn" @click="patch('keyword', filters.keyword)">
          <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          搜索
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.complex-filter {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 4px;
  border: 1px solid #ebeef5;
  padding: 10px 16px;
  margin-bottom: 12px;
  gap: 8px;
  font-size: 13px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: nowrap;
  white-space: nowrap;
  overflow-x: auto;
}

/* 隐藏滚动条让视觉更干净 */
.filter-row::-webkit-scrollbar {
  display: none;
}
.filter-row {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.row-label {
  color: #888;
  white-space: nowrap;
}

.ml-auto {
  margin-left: auto;
}

.tab-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tab-item {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 3px;
  color: #666;
  font-size: 13px;
  transition: all 0.2s;
}

.tab-item:hover {
  background-color: #e6f2fa;
  color: #3498db;
}

.tab-item.active {
  background-color: #3498db;
  color: #fff;
}

.control {
  font-size: 13px;
  height: 28px;
  border: 1px solid #dcdfe6;
  border-radius: 3px;
  background: #fff;
  color: #333;
  padding: 0 8px;
  box-sizing: border-box;
}

.select-control {
  min-width: 100px;
  cursor: pointer;
}

.search-input {
  width: 180px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #555;
  cursor: pointer;
  white-space: nowrap;
}

.status-row {
  margin-top: 4px;
}

.status-text {
  color: #999;
}

.status-val {
  color: #555;
}

.help-link {
  color: #3498db;
  text-decoration: none;
  margin-left: 8px;
}

.help-link:hover {
  text-decoration: underline;
}

.action-row {
  justify-content: space-between;
  border-top: 1px dashed #ebeef5;
  padding-top: 8px;
  margin-top: 2px;
}

.total-text {
  color: #333;
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.clear-btn {
  color: #666;
  text-decoration: none;
  cursor: pointer;
}

.clear-btn:hover {
  color: #3498db;
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #3498db;
  color: white;
  border: none;
  height: 28px;
  padding: 0 14px;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-btn:hover {
  background-color: #2980b9;
}
</style>
