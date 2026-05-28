<template>
  <div class="teams-page">
    <div class="header">
      <h1>🌐 组织大厅</h1>
      <button class="btn btn-primary" @click="showCreateModal = true">创建新组织</button>
    </div>

    <div class="teams-grid">
      <div class="team-card card glass" v-for="team in teams" :key="team.id">
        <h3 class="team-name">{{ team.name }}</h3>
        <p class="team-desc">{{ team.description || '暂无简介' }}</p>
        
        <div class="team-actions">
          <button class="btn btn-outline" @click="joinTeam(team.id)">申请加入</button>
        </div>
      </div>
    </div>

    <!-- Create Team Modal -->
    <div class="modal" v-if="showCreateModal">
      <div class="modal-content card glass">
        <h2>创建新组织</h2>
        <div class="form-group">
          <label>组织名称</label>
          <input type="text" v-model="newTeam.name" class="form-control" />
        </div>
        <div class="form-group">
          <label>简介 (选填)</label>
          <textarea v-model="newTeam.description" class="form-control"></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn btn-outline" @click="showCreateModal = false">取消</button>
          <button class="btn btn-primary" @click="createTeam">创建</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authStore } from '../stores/authStore'

const teams = ref([])
const showCreateModal = ref(false)
const newTeam = ref({ name: '', description: '' })

async function fetchTeams() {
  const res = await fetch('http://localhost:8000/api/groups')
  teams.value = await res.json()
}

async function createTeam() {
  if (!authStore.isAuthenticated) return alert("请先登录")
  if (!newTeam.value.name) return alert('名称不能为空')
  const res = await fetch('http://localhost:8000/api/groups', {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    },
    body: JSON.stringify(newTeam.value)
  })
  if (res.ok) {
    showCreateModal.value = false
    newTeam.value = { name: '', description: '' }
    fetchTeams()
  } else {
    const err = await res.json()
    alert(err.detail || '创建失败')
  }
}

async function joinTeam(groupId) {
  if (!authStore.isAuthenticated) return alert("请先登录")
  const res = await fetch(`http://localhost:8000/api/groups/${groupId}/join`, {
    method: 'POST',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    },
    body: JSON.stringify({})
  })
  if (res.ok) {
    alert("加入成功！")
  } else {
    alert("加入失败")
  }
}

onMounted(() => {
  fetchTeams()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.teams-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.team-card {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}

.team-name {
  margin: 0 0 0.5rem;
  color: var(--primary-color);
}

.team-desc {
  color: var(--text-secondary);
  flex-grow: 1;
  margin-bottom: 1.5rem;
}

.team-actions {
  display: flex;
  justify-content: flex-end;
}

.modal {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  width: 400px;
  padding: 2rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>
