<script setup>
import { onMounted, ref } from 'vue'
import { getSubmission } from '../api/submissions'
import SubmissionDetail from '../components/submission/SubmissionDetail.vue'
import { currentRoute } from '../router'

const submission = ref(null)

onMounted(async () => {
  submission.value = await getSubmission(currentRoute.value.params.sid)
})
</script>

<template>
  <section class="page-grid">
    <SubmissionDetail :submission="submission" />
    <div class="panel">
      <h2>测试点结果</h2>
      <p>后端单测试点详情接口预留中；已有 submission_results 表，后续补 API 即可展示。</p>
    </div>
  </section>
</template>
