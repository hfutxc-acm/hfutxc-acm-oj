<script setup>
import { ref, onMounted } from 'vue'

// 定义一个响应式变量，用来存后端传回来的题目列表
const problemList = ref([])

// 页面一加载完 (onMounted)，就去向 FastAPI 请求数据
onMounted(async () => {
  try {
    // 这里填入你 FastAPI 的地址
    const response = await fetch('http://127.0.0.1:8000/api/problems')
    const data = await response.json()
    // 把拿到的假数据赋值给 problemList
    problemList.value = data
  } catch (error) {
    console.error("请求后端失败，请检查 FastAPI 是否启动:", error)
  }
})
</script>

<template>
  <div class="oj-container">
    <h1>题库列表</h1>

    <table class="oj-table">
      <thead>
        <tr>
          <th>题目 ID</th>
          <th>题目名称</th>
          <th>难度</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="problem in problemList" :key="problem.id">
          <td>{{ problem.id }}</td>
          <td>{{ problem.title }}</td>
          <td>
            <span class="difficulty-tag">{{ problem.difficulty }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
/* 随便写一点基础样式，让它看起来不像上个世纪的网页 */
.oj-container {
  max-width: 800px;
  margin: 40px auto;
  font-family: sans-serif;
}
.oj-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.oj-table th, .oj-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}
.oj-table th {
  background-color: #f4f4f4;
}
.difficulty-tag {
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}
</style>