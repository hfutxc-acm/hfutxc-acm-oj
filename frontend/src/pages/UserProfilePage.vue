<template>
  <div class="user-profile-page" v-if="user">
    <div class="profile-header card glass">
      <div class="avatar-section" :class="{ 'can-edit': canEditAvatar }" @click="triggerUpload">
        <img :src="getAvatarUrl(user)" alt="Avatar" class="avatar-img" />
        <div class="avatar-overlay" v-if="canEditAvatar">
          <span>📸 更换头像</span>
        </div>
        <input type="file" ref="fileInput" style="display: none" accept="image/*" @change="handleFileUpload" />
      </div>
      <div class="info-section">
        <h1 class="username">
          {{ user.username }} 
          <span class="role-badge" :class="user.role">
            {{ user.role === 'super_admin' ? '超级管理员' : (user.role === 'admin' ? '教师/管理员' : '学生') }}
          </span>
        </h1>
        <p class="join-date">加入时间: {{ new Date(user.created_at).toLocaleDateString() }}</p>
        <div class="teams-list">
          <span class="team-tag" v-for="team in user.groups" :key="team.id">
            🛡️ {{ team.name }}
          </span>
          <span v-if="user.groups.length === 0" class="no-teams">暂未加入任何组织</span>
        </div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card card glass">
        <h3>🏆 解题成就</h3>
        <div class="stat-number">{{ user.ac_count }} / {{ user.submissions_count }}</div>
        <p class="stat-desc">AC 题数 / 总提交数</p>
      </div>
      <div class="stat-card card glass">
        <h3>🔥 活跃度评分</h3>
        <div class="stat-number">{{ Math.floor((user.ac_count / (user.submissions_count || 1)) * 100) }}%</div>
        <p class="stat-desc">代码通过率 (AC Rate)</p>
      </div>
    </div>
  </div>
  <div v-else class="loading">加载中...</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { currentRoute, navigateTo } from '../router.js'
import { useAuthStore } from '../stores/authStore'
import { usersApi } from '../api/users'

const user = ref(null)
const fileInput = ref(null)

const canEditAvatar = computed(() => {
  if (!useAuthStore().isAuthenticated) return false
  return useAuthStore().currentUser?.id === user.value?.id || ['admin', 'super_admin'].includes(useAuthStore().currentUser?.role)
})

function getAvatarUrl(u) {
  if (u.avatar_url) {
    return u.avatar_url.startsWith('/') ? `http://localhost:8000${u.avatar_url}` : u.avatar_url
  }
  return 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + u.username
}

function triggerUpload() {
  if (canEditAvatar.value) {
    fileInput.value.click()
  }
}

async function handleFileUpload(event) {
  const file = event.target.files[0]
  if (!file) return
  
  try {
    const data = await usersApi.uploadAvatar(user.value.id, file)
    user.value.avatar_url = data.avatar_url
    if (useAuthStore().currentUser?.id === user.value.id) {
      useAuthStore().currentUser.avatar_url = data.avatar_url
    }
    alert("头像更换成功！")
  } catch (e) {
    alert(e.message || "上传失败")
  } finally {
    event.target.value = ''
  }
}

onMounted(async () => {
  try {
    let uid = currentRoute.value.params.uid
    if (currentRoute.value.name === 'me') {
      if (!useAuthStore().isAuthenticated) {
        alert("请先登录")
        navigateTo('/auth')
        return
      }
      uid = useAuthStore().currentUser?.id
    }
    if (!uid) {
      alert("用户不存在")
      navigateTo('/')
      return
    }
    const data = await usersApi.getUserProfile(uid)
    user.value = data
  } catch (e) {
    alert(e.message || "用户不存在")
  }
})
</script>

<style scoped>
.user-profile-page {
  max-width: 900px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease-out;
}

.profile-header {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-section {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid var(--primary-color);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.avatar-section.can-edit {
  cursor: pointer;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.avatar-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 600;
  opacity: 0;
  transition: opacity 0.2s;
}

.avatar-section.can-edit:hover .avatar-overlay {
  opacity: 1;
}

.info-section {
  flex: 1;
}

.username {
  font-size: 2.5rem;
  margin: 0 0 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.role-badge {
  font-size: 1rem;
  padding: 0.2rem 0.8rem;
  border-radius: 20px;
  background: var(--surface-light);
  color: var(--text-secondary);
}

.role-badge.admin {
  background: var(--danger-color);
  color: white;
}

.join-date {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.teams-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.team-tag {
  background: var(--primary-color);
  color: var(--bg-color);
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.no-teams {
  color: var(--text-muted);
  font-style: italic;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  text-align: center;
  padding: 2rem;
}

.stat-card h3 {
  margin: 0 0 1rem;
  color: var(--text-secondary);
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-desc {
  margin-top: 0.5rem;
  color: var(--text-muted);
}
</style>
