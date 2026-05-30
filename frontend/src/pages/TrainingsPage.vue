<script setup>
import { computed, onMounted, ref } from 'vue'
import { getTrainings } from '../api/trainings'
import TrainingCard from '../components/training/TrainingCard.vue'

const trainings = ref([])
const activeCategory = ref('all')

onMounted(async () => {
  trainings.value = await getTrainings()
})

const categoriesDef = [
  { key: 'novice', label: '新手路线', types: ['新生入门'] },
  { key: 'topic', label: '专题训练', types: ['专题训练'] },
  { key: 'contest', label: '比赛复盘训练', types: ['校赛补题'] },
  { key: 'homework', label: '队内作业', types: ['队内作业'] }
]

// 侧边栏菜单定义，包含动态统计数量
const menuItems = computed(() => {
  const allCount = trainings.value.length
  const items = [
    { key: 'all', label: '全部训练', count: allCount }
  ]
  
  categoriesDef.forEach(cat => {
    const count = trainings.value.filter(t => cat.types.includes(t.type)).length
    items.push({
      key: cat.key,
      label: cat.label,
      count
    })
  })
  
  return items.filter(item => item.key === 'all' || item.count > 0)
})

const categorizedTrainings = computed(() => {
  return categoriesDef.map(cat => ({
    ...cat,
    items: trainings.value.filter(t => cat.types.includes(t.type))
  })).filter(cat => cat.items.length > 0)
})

// 根据当前激活分类过滤展示的分类大类
const visibleCategories = computed(() => {
  if (activeCategory.value === 'all') {
    return categorizedTrainings.value
  }
  return categorizedTrainings.value.filter(cat => cat.key === activeCategory.value)
})
</script>

<template>
  <div class="trainings-layout-container" style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;">
    <!-- 左边栏：分类大导航 -->
    <aside class="trainings-sidebar-wrap">
      <div class="trainings-sidebar">
        <h3 class="sidebar-title">分类导航</h3>
        <div class="sidebar-menu">
          <button
            v-for="item in menuItems"
            :key="item.key"
            class="menu-item"
            :class="{ active: activeCategory === item.key }"
            @click="activeCategory = item.key"
          >
            <span class="menu-label">{{ item.label }}</span>
            <span class="badge-count">{{ item.count }}</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- 右边栏：卡片大盘内容区 -->
    <div class="trainings-content-wrap">
      <div class="page-heading">
        <p class="eyebrow">Training Center</p>
        <h1>训练中心</h1>
        <p>按阶段、分专题的系统化刷题路线。完成各阶段任务以解锁更多权限与称号。</p>
      </div>

      <div class="trainings-main-list">
        <div 
          v-for="category in visibleCategories" 
          :key="category.key" 
          class="training-category"
        >
          <h2 class="category-heading">{{ category.label }}</h2>
          <div class="card-grid">
            <TrainingCard 
              v-for="training in category.items" 
              :key="training.id" 
              :training="training" 
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trainings-layout-container {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 24px;
  align-items: start;
  width: 100%;
}

.trainings-sidebar-wrap {
  position: sticky;
  top: 86px;
}

.trainings-sidebar {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
}

.sidebar-title {
  font-size: 0.85rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--muted);
  letter-spacing: 0.05em;
  margin: 0 0 12px 0;
  border-bottom: 1px dashed var(--border);
  padding-bottom: 6px;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.menu-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 36px;
  padding: 0 12px;
  background: transparent;
  border: none;
  border-radius: 6px;
  color: var(--text);
  font-size: 0.9rem;
  font-weight: 500;
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

.badge-count {
  font-size: 0.75rem;
  background: var(--panel-soft);
  border: 1px solid var(--border);
  color: var(--muted);
  padding: 1px 6px;
  border-radius: 999px;
  font-weight: 600;
}

.menu-item.active .badge-count {
  background: var(--panel);
  border-color: var(--border);
  color: var(--primary-dark);
}

.trainings-content-wrap {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.trainings-main-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.category-heading {
  font-size: 1.25rem;
  margin: 0 0 12px 0;
  font-weight: 800;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
  color: var(--heading-text);
  letter-spacing: -0.01em;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

/* 响应式适配 */
@media (max-width: 992px) {
  .trainings-layout-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .trainings-sidebar-wrap {
    position: static;
  }
}
</style>
