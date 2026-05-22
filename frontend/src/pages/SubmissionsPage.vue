<script setup>
import { onMounted, ref } from 'vue'
import { getSubmissions } from '../api/submissions'
import SubmissionTable from '../components/submission/SubmissionTable.vue'
import Pagination from '../components/common/Pagination.vue'

const submissions = ref([])

onMounted(async () => {
  submissions.value = await getSubmissions()
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Submissions</p>
      <h1>全站提交记录</h1>
      <p>查看最近代码提交和评测状态。</p>
    </div>
    <SubmissionTable :submissions="submissions" />
    <Pagination :total="submissions.length" />
  </section>
</template>
