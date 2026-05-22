<script setup>
import { ref } from 'vue'
import { submitCode } from '../../api/problems'

const props = defineProps({
  problemId: [String, Number]
})

const emit = defineEmits(['submitted'])

const language = ref('cpp')
const code = ref(`#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    return 0;
}`)
const message = ref('')
const saving = ref(false)

async function handleSubmit() {
  if (!props.problemId) return
  saving.value = true
  message.value = '提交中...'
  try {
    const result = await submitCode({
      userId: 1,
      problemId: props.problemId,
      language: language.value,
      code: code.value
    })
    message.value = `提交成功，运行 ID #${result.submission_id}`
    emit('submitted', result)
  } catch (error) {
    message.value = error.message
  } finally {
    saving.value = false
  }
}

function resetCode() {
  code.value = ''
  message.value = ''
}
</script>

<template>
  <section class="submit-panel">
    <div class="section-title-row">
      <h2>提交代码</h2>
      <select v-model="language" class="control compact-control">
        <option value="cpp">C++17</option>
        <option value="python">Python 3</option>
      </select>
    </div>
    <textarea v-model="code" class="code-area" spellcheck="false"></textarea>
    <div class="action-row">
      <button class="primary-btn" :disabled="saving" @click="handleSubmit">{{ saving ? '提交中...' : '提交' }}</button>
      <button class="ghost-btn" @click="resetCode">重置</button>
      <span v-if="message" class="form-message">{{ message }}</span>
    </div>
  </section>
</template>
