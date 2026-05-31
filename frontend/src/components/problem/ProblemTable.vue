<script setup>
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'
import DifficultyBadge from './DifficultyBadge.vue'
import { navigateTo } from '../../router'

defineProps({
  problems: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
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
    </table>
    <!-- Virtual scroller for large lists -->
    <RecycleScroller
      v-if="problems.length > 50"
      class="virtual-list"
      :items="problems"
      :item-size="52"
      key-field="id"
      v-slot="{ item: problem }"
    >
      <div class="virtual-row" @click="navigateTo(`/problems/${problem.id}`)">
        <div class="v-status">
          <svg v-if="problem.status === 'AC'" viewBox="0 0 24 24" width="18" height="18" stroke="var(--success)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span v-else class="status-dash">-</span>
        </div>
        <div class="v-id">#{{ problem.id }}</div>
        <div class="v-title">
          <span class="title-text">{{ problem.title }}</span>
          <span v-for="tag in problem.tags" :key="tag" class="capsule-tag">{{ tag }}</span>
        </div>
        <div class="v-diff"><DifficultyBadge :difficulty="problem.difficulty" /></div>
        <div class="v-pass">
          <div class="progress-bar"><div class="progress-fill" :style="{ width: `${problem.passRate}%` }"></div></div>
          <span class="progress-text">{{ problem.passRate }}%</span>
        </div>
      </div>
    </RecycleScroller>
    <!-- Normal table for small lists -->
    <table v-else class="data-table data-table-body">
      <tbody>
        <tr v-for="problem in problems" :key="problem.id" class="problem-row">
          <td class="status-cell">
            <svg v-if="problem.status === 'AC'" viewBox="0 0 24 24" width="18" height="18" stroke="var(--success)" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" class="status-icon"><polyline points="20 6 9 17 4 12"></polyline></svg>
            <span v-else class="status-dash">-</span>
          </td>
          <td class="id-cell">#{{ problem.id }}</td>
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
  width: 100%;
  overflow-x: auto;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th, .data-table td {
  padding: 14px 18px;
  border-bottom: 1px solid var(--table-td-border);
  white-space: nowrap;
  color: var(--table-td-text);
  font-size: 0.9rem;
}

.data-table th {
  background-color: var(--table-th-bg);
  color: var(--table-th-text);
  font-weight: 800;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid var(--border);
}

.status-th { width: 70px; text-align: center; }
.id-th { width: 90px; }
.diff-th { width: 130px; }
.pass-th { width: 160px; }

.problem-row {
  transition: background-color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.problem-row:hover {
  background-color: var(--table-hover-bg);
}

.problem-row:last-child td {
  border-bottom: none;
}

.status-cell {
  text-align: center;
}

.status-icon {
  display: inline-block;
  vertical-align: middle;
}

.status-dash {
  color: var(--muted);
  font-weight: bold;
}

.id-cell {
  color: var(--muted);
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-weight: 600;
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
  color: var(--text);
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: color 0.2s;
  text-align: left;
}

.title-btn:hover {
  color: var(--primary);
}

.inline-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.capsule-tag {
  background-color: var(--nav-btn-active-bg);
  color: var(--primary-dark);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 700;
  white-space: nowrap;
}

.progress-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: var(--panel-soft);
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid var(--border);
}

.progress-fill {
  height: 100%;
  background-color: var(--primary);
  border-radius: 999px;
}

.progress-text {
  font-size: 0.8rem;
  color: var(--muted);
  font-weight: 700;
  min-width: 38px;
  text-align: right;
}

/* Virtual scroller styles */
.virtual-list {
  height: 600px;
  overflow-y: auto;
}

.virtual-row {
  display: grid;
  grid-template-columns: 70px 90px 1fr 130px 160px;
  align-items: center;
  padding: 0 18px;
  height: 52px;
  border-bottom: 1px solid var(--table-td-border);
  cursor: pointer;
  transition: background-color 0.2s;
}

.virtual-row:hover {
  background-color: var(--table-hover-bg);
}

.v-status { text-align: center; }
.v-id { color: var(--muted); font-family: ui-monospace, monospace; font-weight: 600; font-size: 0.9rem; }
.v-title { display: flex; align-items: center; gap: 8px; overflow: hidden; }
.v-title .title-text { font-weight: 700; font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.v-diff { }
.v-pass { display: flex; align-items: center; gap: 10px; }

.data-table-body { border-top: none; }
</style>
