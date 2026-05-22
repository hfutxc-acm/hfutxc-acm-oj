<script setup>
import DifficultyBadge from './DifficultyBadge.vue'
import ProblemTag from './ProblemTag.vue'
import { navigateTo } from '../../router'

defineProps({
  problems: { type: Array, default: () => [] }
})

function statusLabel(status) {
  if (status === 'AC') return '已通过'
  if (status === 'TRIED') return '尝试过'
  return '未尝试'
}
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead>
        <tr>
          <th>状态</th>
          <th>题号</th>
          <th>标题</th>
          <th>难度</th>
          <th>标签</th>
          <th>通过数</th>
          <th>提交数</th>
          <th>通过率</th>
          <th>来源</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="problem in problems" :key="problem.id">
          <td><span :class="['status-dot', problem.status]">{{ statusLabel(problem.status) }}</span></td>
          <td>#{{ problem.id }}</td>
          <td>
            <button class="link-button" @click="navigateTo(`/problems/${problem.id}`)">{{ problem.title }}</button>
          </td>
          <td><DifficultyBadge :difficulty="problem.difficulty" /></td>
          <td class="tag-cell"><ProblemTag v-for="tag in problem.tags" :key="tag" :tag="tag" /></td>
          <td>{{ problem.accepted }}</td>
          <td>{{ problem.submissions }}</td>
          <td>{{ problem.passRate }}%</td>
          <td>{{ problem.source }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
