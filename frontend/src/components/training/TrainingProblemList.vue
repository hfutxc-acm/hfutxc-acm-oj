<script setup>
import DifficultyBadge from '../problem/DifficultyBadge.vue'
import ProblemTag from '../problem/ProblemTag.vue'
import { navigateTo } from '../../router'

defineProps({
  problems: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap">
    <table class="data-table">
      <thead><tr><th>顺序</th><th>题号</th><th>标题</th><th>难度</th><th>标签</th><th>状态</th></tr></thead>
      <tbody>
        <tr v-for="problem in problems" :key="problem.id">
          <td>{{ problem.order }}</td>
          <td>#{{ problem.id }}</td>
          <td><button class="link-button" @click="navigateTo(`/problems/${problem.id}`)">{{ problem.title }}</button></td>
          <td><DifficultyBadge :difficulty="problem.difficulty" /></td>
          <td class="tag-cell"><ProblemTag v-for="tag in problem.tags" :key="tag" :tag="tag" /></td>
          <td>{{ problem.status === 'AC' ? '已通过' : problem.status === 'TRIED' ? '尝试过' : '未尝试' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
