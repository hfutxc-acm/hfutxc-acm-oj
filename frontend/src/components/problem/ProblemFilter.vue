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

// 难度对应的颜色点指示器
const diffColors = {
  '入门': '#22c55e',       // 绿色
  '普及-': '#3b82f6',      // 蓝色
  '普及': '#a855f7',       // 紫色
  '提高': '#f97316',       // 橙色
  '省选': '#ef4444',       // 红色
  'ICPC区域赛': '#1e293b'   // 深色
}

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
    source: '全部',
    searchContent: false
  })
}
</script>

<template>
  <aside class="filter-sidebar" style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;">
    <!-- 搜索板块 -->
    <div class="filter-section">
      <h3 class="section-title">搜索题目</h3>
      <div class="search-box">
        <div class="input-wrap">
          <input
            :value="filters.keyword"
            class="control search-input"
            placeholder="搜算法、标题或编号..."
            @input="patch('keyword', $event.target.value)"
          />
          <span class="search-icon">🔍</span>
        </div>
        <label class="checkbox-label">
          <input type="checkbox" :checked="filters.searchContent" @change="patch('searchContent', $event.target.checked)" />
          <span>搜索题面内容</span>
        </label>
      </div>
    </div>

    <!-- 所属题库 -->
    <div class="filter-section">
      <h3 class="section-title">所属题库</h3>
      <div class="sidebar-menu">
        <button
          v-for="src in sources"
          :key="src"
          class="menu-item"
          :class="{ active: filters.source === src }"
          @click="patch('source', src)"
        >
          <span class="menu-label">{{ src }}</span>
        </button>
      </div>
    </div>

    <!-- 题目难度 -->
    <div class="filter-section">
      <h3 class="section-title">题目难度</h3>
      <div class="sidebar-menu">
        <button
          v-for="diff in difficulties"
          :key="diff"
          class="menu-item"
          :class="{ active: filters.difficulty === diff }"
          @click="patch('difficulty', diff)"
        >
          <span 
            v-if="diff !== '全部'" 
            class="color-dot" 
            :style="{ backgroundColor: diffColors[diff] }"
          ></span>
          <span class="menu-label">{{ diff }}</span>
        </button>
      </div>
    </div>

    <!-- 算法标签 -->
    <div class="filter-section">
      <h3 class="section-title">算法标签</h3>
      <div class="tag-cloud">
        <button
          v-for="tg in tags"
          :key="tg"
          class="sidebar-tag"
          :class="{ active: filters.tag === tg }"
          @click="patch('tag', tg)"
        >
          {{ tg }}
        </button>
      </div>
    </div>

    <!-- 做题状态 -->
    <div class="filter-section">
      <h3 class="section-title">做题状态</h3>
      <div class="sidebar-menu">
        <button
          v-for="stat in statuses"
          :key="stat"
          class="menu-item"
          :class="{ active: filters.status === stat }"
          @click="patch('status', stat)"
        >
          <span v-if="stat === '已 AC'" class="status-indicator ac">✓</span>
          <span v-else-if="stat === '尝试过'" class="status-indicator tried">!</span>
          <span v-else-if="stat === '收藏'" class="status-indicator fav">★</span>
          <span v-else class="status-indicator dot"></span>
          <span class="menu-label">{{ stat }}</span>
        </button>
      </div>
    </div>

    <!-- 边栏页脚统计与清除 -->
    <div class="sidebar-footer">
      <span class="total-count">共 {{ total }} 道题目</span>
      <button class="clear-link-btn" @click="clearFilters">重置筛选</button>
    </div>
  </aside>
</template>

<style scoped>
.filter-sidebar {
  display: flex;
  flex-direction: column;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  gap: 20px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
  align-self: start;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-title {
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--muted);
  letter-spacing: 0.05em;
  margin: 0 0 4px 0;
  border-bottom: 1px dashed var(--border);
  padding-bottom: 6px;
}

/* 搜索框 */
.search-box {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-wrap {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding-right: 32px;
  height: 36px;
  font-size: 0.9rem;
  background: var(--panel-soft);
  border-color: var(--border);
}

.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted);
  font-size: 0.9rem;
  pointer-events: none;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: var(--muted);
  cursor: pointer;
  user-select: none;
}

.checkbox-label input {
  cursor: pointer;
}

/* 侧边栏垂直菜单 */
.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  height: 34px;
  padding: 0 10px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: var(--text);
  font-size: 0.9rem;
  font-weight: 500;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-item:hover {
  background: var(--panel-soft);
  color: var(--primary);
}

.menu-item.active {
  background: var(--nav-btn-active-bg);
  color: var(--primary-dark);
  font-weight: 700;
}

/* 状态和难度指示器 */
.color-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  font-size: 0.75rem;
  font-weight: bold;
  flex-shrink: 0;
}

.status-indicator.ac {
  color: var(--success);
}

.status-indicator.tried {
  color: var(--danger);
}

.status-indicator.fav {
  color: var(--warning);
}

.status-indicator.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--border);
}

/* 标签云 */
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.sidebar-tag {
  background: var(--panel-soft);
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.sidebar-tag:hover {
  border-color: var(--primary);
  color: var(--primary);
  background: var(--panel);
}

.sidebar-tag.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
}

/* 边栏页脚 */
.sidebar-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border);
  padding-top: 12px;
  margin-top: 4px;
  font-size: 0.8rem;
}

.total-count {
  color: var(--muted);
  font-weight: 600;
}

.clear-link-btn {
  background: transparent;
  border: none;
  color: var(--primary);
  cursor: pointer;
  font-weight: 700;
  padding: 0;
  font-size: 0.8rem;
}

.clear-link-btn:hover {
  text-decoration: underline;
}
</style>
