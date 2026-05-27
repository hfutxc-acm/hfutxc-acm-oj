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
    <div class="page-heading">
      <p class="eyebrow">Submission Status</p>
      <h1>测评结果</h1>
    </div>
    <SubmissionDetail :submission="submission" />
    <div class="panel">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2>测试点详情</h2>
        <span class="badge" style="background: var(--surface-2); border: 1px solid var(--border-color); color: var(--text-2);">当前为：训练模式</span>
      </div>
      <div style="background: var(--surface-2); border-radius: 8px; padding: 1rem; border: 1px solid var(--border-color);">
        <p style="margin-bottom: 0.5rem;"><strong>第一个错误点：#8</strong></p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
          <div>
            <span style="color: var(--text-2); font-size: 0.85rem;">期望输出</span>
            <pre style="margin-top: 0.25rem;">12345</pre>
          </div>
          <div>
            <span style="color: var(--text-2); font-size: 0.85rem;">实际输出</span>
            <pre style="margin-top: 0.25rem;">12340</pre>
          </div>
        </div>
        <p style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-2);">提示：训练模式下提供详细错误信息以辅助学习，比赛模式下将严格隐藏测试点细节。</p>
      </div>
    </div>
  </section>
</template>
