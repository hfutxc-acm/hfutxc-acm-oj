<script setup>
const props = defineProps({
  status: { type: String, default: 'Pending' }
})

function label(status) {
  const map = {
    AC: 'Accepted',
    WA: 'Wrong Answer',
    TLE: 'Time Limit Exceeded',
    MLE: 'Memory Limit Exceeded',
    RE: 'Runtime Error',
    CE: 'Compilation Error',
    Pending: 'Pending',
    Judging: 'Judging',
    SE: 'System Error'
  }
  return map[status] || status
}
</script>

<template>
  <span :class="['verdict', `verdict-${props.status}`]">{{ label(props.status) }}</span>
</template>
