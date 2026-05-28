<template>
  <div class="admin-users-page">
    <div class="header">
      <h1>👥 用户权限管理</h1>
      <p>管理全站用户的角色和身份。</p>
    </div>

    <div class="card glass">
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>当前角色</th>
            <th>注册时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>
              <div class="user-info">
                <img :src="user.avatar_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + user.username" class="small-avatar" />
                {{ user.username }}
              </div>
            </td>
            <td>
              <span class="role-badge" :class="user.role">{{ user.role === 'admin' ? '管理员' : '学生' }}</span>
            </td>
            <td>{{ new Date(user.created_at).toLocaleDateString() }}</td>
            <td>
              <button 
                v-if="user.role === 'user'" 
                class="btn btn-sm btn-outline danger" 
                @click="updateRole(user.id, 'admin')">
                提拔为管理
              </button>
              <button 
                v-if="user.role === 'admin'" 
                class="btn btn-sm btn-outline" 
                @click="updateRole(user.id, 'user')">
                撤销管理
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authStore } from '../../stores/authStore'

const users = ref([])

async function fetchUsers() {
  const res = await fetch('http://localhost:8000/api/admin/users', {
    headers: { 'Authorization': `Bearer ${authStore.token}` }
  })
  if (res.ok) {
    users.value = await res.json()
  }
}

async function updateRole(userId, newRole) {
  if (!confirm(`确定要将该用户设为 ${newRole} 吗？`)) return
  const res = await fetch(`http://localhost:8000/api/admin/users/${userId}/role`, {
    method: 'PUT',
    headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${authStore.token}`
    },
    body: JSON.stringify({ role: newRole })
  })
  if (res.ok) {
    fetchUsers()
  } else {
    alert("更新失败")
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.header {
  margin-bottom: 2rem;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th, .users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.users-table th {
  color: var(--text-secondary);
  font-weight: 600;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.small-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
}

.role-badge {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.85rem;
  background: var(--surface-light);
}

.role-badge.admin {
  background: var(--danger-color);
  color: white;
}

.btn-sm {
  padding: 0.3rem 0.8rem;
  font-size: 0.85rem;
}

.btn-outline.danger {
  border-color: var(--danger-color);
  color: var(--danger-color);
}
.btn-outline.danger:hover {
  background: var(--danger-color);
  color: white;
}
</style>
