<script setup>
import DifficultyBadge from './DifficultyBadge.vue'
import { navigateTo } from '../../router'

defineProps({
  problems: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap" style="font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;">
    <table class="data-table">
      <thead>
        <tr>
          <th class="status-th">状态</th>
          <th class="id-th">题号</th>
          <th>题目名称</th>
          <th class="diff-th">难度</th>
          <th class="pass-th">通过率</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="problem in problems" :key="problem.id" class="problem-row">
          <td class="status-cell">
            <svg v-if="problem.status === 'AC'" viewBox="0 0 24 24" width="20" height="20" stroke="#52c41a" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" class="status-icon"><polyline points="20 6 9 17 4 12"></polyline></svg>
            <span v-else class="status-dash">-</span>
          </td>
          <td class="id-cell">{{ problem.id }}</td>
          <td>
            <div class="title-cell">
              <button class="link-button title-btn" @click="navigateTo(`/problems/${problem.id}`)">{{ problem.title }}</button>
              <div class="inline-tags">
                <span v-for="tag in problem.tags" :key="tag" class="capsule-tag">{{ tag }}</span>
              </div>
            </div>
          </td>
          <td><DifficultyBadge :difficulty="problem.difficulty" /></td>
          <td>
            <div class="progress-wrap" :title="`${problem.passRate}% (${problem.accepted}/${problem.submissions})`">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${problem.passRate}%` }"></div>
              </div>
              <span class="progress-text">{{ problem.passRate }}%</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-wrap {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #ebeef5;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th, .data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
}

.data-table th {
  background-color: #fafafa;
  color: #606266;
  font-weight: 500;
  font-size: 0.95rem;
}

.status-th { width: 60px; text-align: center; }
.id-th { width: 80px; }
.diff-th { width: 120px; }
.pass-th { width: 150px; }

.problem-row {
  transition: background-color 0.3s;
}

.problem-row:hover {
  background-color: #e6f7ff; /* 淡蓝色 */
}

.status-cell {
  text-align: center;
}

.status-icon {
  display: inline-block;
  vertical-align: middle;
}

.status-dash {
  color: #c0c4cc;
  font-weight: bold;
}

.id-cell {
  color: #666;
  font-family: Monaco, Consolas, monospace;
}

.title-cell {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.title-btn {
  background: none;
  border: none;
  padding: 0;
  color: #333;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.title-btn:hover {
  color: #3498db;
}

.inline-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.capsule-tag {
  background-color: #2db7f5; /* 青绿色 */
  color: #fff;
  padding: 1px 6px;
  border-radius: 3px; /* 极小圆角 */
  font-size: 0.75rem; /* 较小字体 */
  white-space: nowrap;
}

.progress-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #f0f0f0; /* 灰色底色 */
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #3498db; /* 蓝色填充 */
  border-radius: 4px;
}

.progress-text {
  font-size: 0.85rem;
  color: #666;
  min-width: 40px;
  text-align: right;
}
</style>
