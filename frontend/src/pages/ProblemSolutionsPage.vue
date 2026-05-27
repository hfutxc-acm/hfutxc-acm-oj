<script setup>
import { ref, onMounted } from 'vue'
import { currentRoute, navigateTo } from '../router'
import { getProblem } from '../api/problems'
import { MdPreview, MdCatalog } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'

const problem = ref(null)
const solutions = ref([
  {
    id: 1,
    title: 'O(N) 时间复杂度，C++ 详细注释',
    author: 'Admin',
    likes: 42,
    time: '2023-10-01 10:00',
    content: '这道题的核心在于**前缀和**的应用。\n\n### 思路\n我们可以在 $O(N)$ 的时间复杂度内遍历数组，并在过程中维护一个前缀和数组。\n\n```cpp\n#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    cin >> n;\n    vector<long long> a(n + 1, 0);\n    for (int i = 1; i <= n; i++) {\n        int x;\n        cin >> x;\n        a[i] = a[i - 1] + x;\n    }\n    cout << a[n] << endl;\n    return 0;\n}\n```\n\n### 总结\n注意数据范围，可能会爆 `int`，所以我们使用了 `long long`。'
  },
  {
    id: 2,
    title: 'Python 简短解法',
    author: 'Tourist',
    likes: 15,
    time: '2023-10-02 14:30',
    content: '利用 Python 的内置函数可以非常简短地完成。\n\n```python\nprint(sum(map(int, input().split())))\n```\n如果题目有多行输入，记得使用循环处理。\n\n$$E = mc^2$$ \n公式渲染测试。'
  }
])
const selectedSolution = ref(null)

const id = 'preview-only' // For md-editor-v3 catalog anchor

onMounted(async () => {
  problem.value = await getProblem(currentRoute.value.params.pid)
})
</script>

<template>
  <div class="page-grid">
    <div class="page-heading">
      <p class="eyebrow" style="cursor: pointer" @click="navigateTo(`/problems/${currentRoute.params.pid}`)">
        &larr; 返回 {{ problem ? problem.title : '题目' }}
      </p>
      <h1>题目题解</h1>
      <p>学习他人的思路，提升自己的水平。你也可以<a href="javascript:void(0)" @click="navigateTo(`/solutions/publish?pid=${currentRoute.params.pid}`)">发布题解</a>。</p>
    </div>

    <!-- 题解列表 -->
    <div v-if="!selectedSolution" class="solution-list">
      <div v-if="solutions.length === 0" class="panel">
        <p style="text-align: center; color: var(--muted); padding: 40px 0;">暂无题解，快来做第一个发布的人吧！</p>
      </div>
      <div v-for="sol in solutions" :key="sol.id" class="solution-card panel" @click="selectedSolution = sol">
        <h3 class="sol-title">{{ sol.title }}</h3>
        <div class="sol-meta">
          <span class="author">👤 {{ sol.author }}</span>
          <span class="time">🕒 {{ sol.time }}</span>
          <span class="likes">👍 {{ sol.likes }}</span>
        </div>
      </div>
    </div>

    <!-- 题解详情 -->
    <div v-else class="solution-detail">
      <div class="detail-header panel" style="margin-bottom: 20px;">
        <button class="ghost-btn" style="margin-bottom: 10px;" @click="selectedSolution = null">&larr; 返回列表</button>
        <h2 style="margin: 0 0 10px 0;">{{ selectedSolution.title }}</h2>
        <div class="sol-meta">
          <span class="author">👤 {{ selectedSolution.author }}</span>
          <span class="time">🕒 {{ selectedSolution.time }}</span>
          <span class="likes">👍 {{ selectedSolution.likes }}</span>
        </div>
      </div>
      
      <div class="detail-body">
        <div class="panel article-content">
          <MdPreview :editorId="id" :modelValue="selectedSolution.content" />
        </div>
        <div class="panel catalog-panel">
          <h3 style="margin-top:0;">目录</h3>
          <MdCatalog :editorId="id" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.solution-list {
  display: grid;
  gap: 16px;
}
.solution-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.solution-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-color: var(--primary);
}
.sol-title {
  margin: 0 0 10px 0;
  color: var(--text);
  font-size: 1.1rem;
}
.sol-meta {
  display: flex;
  gap: 16px;
  font-size: 0.85rem;
  color: var(--muted);
}
.detail-body {
  display: grid;
  grid-template-columns: 1fr 250px;
  gap: 20px;
  align-items: start;
}
.catalog-panel {
  position: sticky;
  top: 80px;
}

@media (max-width: 768px) {
  .detail-body {
    grid-template-columns: 1fr;
  }
  .catalog-panel {
    display: none;
  }
}
</style>
