<template>
  <div class="auth-page">
    <div class="auth-container card glass">
      <div class="tabs">
        <button :class="{ active: isLogin }" @click="isLogin = true">登录</button>
        <button :class="{ active: !isLogin }" @click="isLogin = false">注册</button>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label>用户名</label>
          <input type="text" v-model="form.username" required class="form-control" placeholder="输入你的用户名" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input type="password" v-model="form.password" required class="form-control" placeholder="输入密码" />
        </div>
        
        <div class="error-msg" v-if="errorMsg">{{ errorMsg }}</div>
        
        <button type="submit" class="btn btn-primary submit-btn" :disabled="loading">
          {{ loading ? '请稍候...' : (isLogin ? '立即登录' : '注册账号') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { setToken, initAuth } from '../stores/authStore.js'
import { navigateTo } from '../router.js'

const isLogin = ref(true)
const loading = ref(false)
const errorMsg = ref('')

const form = ref({
  username: '',
  password: ''
})

async function handleSubmit() {
  errorMsg.value = ''
  loading.value = true
  try {
    const endpoint = isLogin.value ? '/api/login' : '/api/register'
    const res = await fetch(`http://localhost:8000${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    
    if (!res.ok) {
      const err = await res.json()
      errorMsg.value = err.detail || '操作失败，请重试'
      return
    }

    if (isLogin.value) {
      const data = await res.json()
      setToken(data.access_token)
      await initAuth() // Fetch user profile and set state
      navigateTo('/')
    } else {
      // Auto login after register
      isLogin.value = true
      handleSubmit()
    }
  } catch (e) {
    errorMsg.value = "网络错误，请检查服务器连接"
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 200px);
}

.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  animation: slideUp 0.4s ease-out;
}

.tabs {
  display: flex;
  margin-bottom: 2rem;
  border-bottom: 2px solid var(--border-color);
}

.tabs button {
  flex: 1;
  background: none;
  border: none;
  padding: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.tabs button.active {
  color: var(--primary-color);
}

.tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--primary-color);
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  margin-top: 1rem;
}

.error-msg {
  color: var(--danger-color);
  font-size: 0.9rem;
  text-align: center;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
