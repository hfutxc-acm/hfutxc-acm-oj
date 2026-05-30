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
              <span class="role-badge" :class="user.role">
                {{ user.role === 'super_admin' ? '超级管理员' : (user.role === 'admin' ? '管理员' : '学生') }}
              </span>
            </td>
            <td>{{ new Date(user.created_at).toLocaleDateString() }}</td>
            <td>
              <template v-if="authStore.currentUser?.role === 'super_admin'">
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
                <button 
                  v-if="user.role !== 'super_admin' && user.id !== authStore.currentUser.id" 
                  class="btn btn-sm btn-outline warning ml-2" 
                  style="margin-left: 0.5rem;"
                  @click="transferAdmin(user.id, user.username)">
                  👑 移交超级管理
                </button>
              </template>
              <span v-else class="text-muted" style="font-size: 0.85rem; color: #888;">无授权</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authStore, initAuth } from '../../stores/authStore'
import { getUsers, updateUserRole, transferSuperAdmin } from '../../api/admin'

const users = ref([])

async function fetchUsers() {
  try {
    users.value = await getUsers()
  } catch (e) {
    console.error(e)
  }
}

async function updateRole(userId, newRole) {
  if (!confirm(`确定要将该用户设为 ${newRole} 吗？`)) return
  try {
    await updateUserRole(userId, newRole)
    fetchUsers()
  } catch (e) {
    alert(e.message || "更新失败")
  }
}

async function transferAdmin(userId, username) {
  const code = prompt(`【高危操作】确定要将“超级管理员”移交给 ${username} 吗？\n一旦移交，您本人将立刻降级为普通管理员，失去后续赋权资格！\n\n如果确认，请输入"我确认移交"：`)
  if (code !== "我确认移交") {
    alert("已取消交接")
    return
  }
  
  try {
    await transferSuperAdmin(userId)
    alert("交接成功！您已被降级为普通管理员。")
    await initAuth() // Refresh current user's role from backend
    fetchUsers()
  } catch (e) {
    alert(e.message || "交接失败")
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
  background: var(--primary-color);
  color: white;
}

.role-badge.super_admin {
  background: var(--danger-color);
  color: white;
  box-shadow: 0 0 10px rgba(255, 71, 87, 0.4);
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

.btn-outline.warning {
  border-color: #ffa502;
  color: #ffa502;
}

.btn-outline.warning:hover {
  background: #ffa502;
  color: white;
}
</style>
