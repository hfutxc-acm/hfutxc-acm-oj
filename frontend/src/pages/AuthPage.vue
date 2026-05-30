<template>
  <div class="auth-page-wrapper">
    <!-- Animated Background Shapes -->
    <div class="shape shape-1"></div>
    <div class="shape shape-2"></div>
    <div class="shape shape-3"></div>

    <div class="auth-container card glass">
      <div class="auth-header">
        <img src="https://upload.wikimedia.org/wikipedia/zh/e/e8/Icpc_logo.png" alt="ICPC Logo" class="logo-icon" />
        <h2>{{ isLogin ? '欢迎回来' : '加入我们' }}</h2>
        <p class="subtitle">HFUTXC ACM Online Judge</p>
      </div>

      <div class="tabs">
        <button :class="{ active: isLogin }" @click="isLogin = true">登录</button>
        <button :class="{ active: !isLogin }" @click="isLogin = false">注册</button>
      </div>

      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="form-group">
          <label>用户名</label>
          <div class="input-wrapper">
            <span class="icon">👤</span>
            <input type="text" v-model="form.username" required class="form-control" placeholder="输入你的用户名" />
          </div>
        </div>
        <div class="form-group">
          <label>密码</label>
          <div class="input-wrapper">
            <span class="icon">🔒</span>
            <input type="password" v-model="form.password" required class="form-control" placeholder="输入密码" />
          </div>
        </div>
        
        <div class="error-msg" v-if="errorMsg">{{ errorMsg }}</div>
        
        <button type="submit" class="btn btn-primary submit-btn" :disabled="loading" :class="{ 'loading-btn': loading }">
          <span>{{ loading ? (isLogin ? '登录中...' : '注册中...') : (isLogin ? '立即登录' : '注册账号') }}</span>
          <div class="loader" v-if="loading"></div>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authStore, setToken } from '../stores/authStore'
import { navigateTo } from '../router'
import { authApi } from '../api/auth'

const isLogin = ref(true)
const loading = ref(false)
const errorMsg = ref('')

const form = ref({
  username: '',
  password: ''
})

async function handleSubmit() {
  if (!form.value.username || !form.value.password) {
    errorMsg.value = '请填写完整信息'
    return
  }
  
  errorMsg.value = ''
  loading.value = true
  
  try {
    if (isLogin.value) {
      const data = await authApi.login(form.value.username, form.value.password)
      setToken(data.access_token)
      authStore.currentUser = { id: data.user_id, role: data.role, username: form.value.username }
      authStore.isAuthenticated = true
      navigateTo('/')
    } else {
      await authApi.register(form.value.username, form.value.password)
      isLogin.value = true
      handleSubmit() // auto login
    }
  } catch (e) {
    errorMsg.value = e.message || "网络错误，请检查服务器连接"
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Wrapper to break out of main layout constraints if necessary, and provide full bg */
.auth-page-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Light theme background by default */
  background: linear-gradient(150deg, #E0F2FF 10%, #C3E6CB 60%, #A5D7FA 90%);
  background-size: 400% 400%;
  animation: gradientBG 10s ease infinite;
  z-index: 100;
}

/* Dark theme background */
:global(.dark) .auth-page-wrapper {
  background: linear-gradient(150deg, #0d1b2a 10%, #0a2e21 60%, #152438 90%);
  background-size: 400% 400%;
  animation: gradientBG 10s ease infinite;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* Floating Shapes */
.shape {
  position: absolute;
  filter: blur(60px); /* Less blur for more punch */
  z-index: 0;
  border-radius: 50%;
  animation: float 10s infinite ease-in-out;
}
.shape-1 {
  width: 400px; height: 400px;
  background: rgba(195, 230, 203, 0.4); /* Lower opacity */
  top: -100px; left: -100px;
}
.shape-2 {
  width: 500px; height: 500px;
  background: rgba(165, 215, 250, 0.3); /* Lower opacity */
  bottom: -150px; right: -100px;
  animation-delay: -5s;
}
.shape-3 {
  width: 300px; height: 300px;
  background: rgba(224, 242, 255, 0.2);
  top: 40%; left: 60%;
  animation-delay: -2s;
  animation-duration: 12s;
}

:global(.dark) .shape-1 { background: rgba(10, 255, 180, 0.4); filter: blur(70px); }
:global(.dark) .shape-2 { background: rgba(64, 156, 255, 0.4); filter: blur(70px); }
:global(.dark) .shape-3 { background: rgba(0, 200, 255, 0.3); filter: blur(70px); }

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(40px) scale(1.1); } /* More movement */
}

/* Glassmorphism Container */
.auth-container {
  width: 100%;
  max-width: 420px;
  padding: 3rem 2.5rem; /* Slightly taller */
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 30px 60px rgba(0,0,0,0.15), inset 0 0 0 1px rgba(255,255,255,0.2);
  border-radius: 24px;
  z-index: 1;
  animation: slideUp 0.8s cubic-bezier(0.2, 1, 0.2, 1);
  color: #222;
  position: relative;
  overflow: hidden;
}

/* Subtle shine effect on the glass box */
.auth-container::before {
  content: '';
  position: absolute;
  top: 0; left: -150%;
  width: 50%; height: 100%;
  background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0) 100%);
  transform: skewX(-25deg);
  animation: shine 6s infinite;
}

@keyframes shine {
  0% { left: -150%; }
  20% { left: 200%; }
  100% { left: 200%; }
}

:global(.dark) .auth-container {
  background: rgba(15, 25, 40, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 30px 60px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.05);
  color: #fff;
}
:global(.dark) .auth-container::before {
  background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%);
}

.auth-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo-icon {
  height: 90px;
  margin-bottom: 1.5rem;
  animation: bounce 3s infinite cubic-bezier(0.28, 0.84, 0.42, 1);
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));
}
:global(.dark) .logo-icon {
  filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5)) brightness(1.2);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.auth-header h2 {
  margin: 0 0 0.5rem;
  font-size: 1.8rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.subtitle {
  color: rgba(0, 0, 0, 0.5);
  font-size: 0.9rem;
}
:global(.dark) .subtitle {
  color: rgba(255, 255, 255, 0.6);
}

/* Tabs */
.tabs {
  display: flex;
  margin-bottom: 2rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
}
:global(.dark) .tabs {
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.tabs button {
  flex: 1;
  background: none;
  border: none;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.4);
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}
:global(.dark) .tabs button {
  color: rgba(255, 255, 255, 0.5);
}

.tabs button.active {
  color: #333;
}
:global(.dark) .tabs button.active {
  color: #fff;
}

.tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 2px;
  background: #333;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
:global(.dark) .tabs button.active::after {
  background: #fff;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
}

/* Form */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group label {
  color: rgba(0, 0, 0, 0.6);
  font-size: 0.9rem;
  margin-bottom: 0.4rem;
  display: block;
}
:global(.dark) .form-group label {
  color: rgba(255, 255, 255, 0.8);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper .icon {
  position: absolute;
  left: 1rem;
  font-size: 1.2rem;
  opacity: 0.7;
}

.form-control {
  width: 100%;
  padding: 0.8rem 1rem 0.8rem 3rem;
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
  color: #333;
  border-radius: 12px;
  transition: all 0.3s;
}
:global(.dark) .form-control {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}

.form-control::placeholder {
  color: rgba(0, 0, 0, 0.3);
}
:global(.dark) .form-control::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-control:focus {
  background: rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 0, 0, 0.2);
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
  outline: none;
}
:global(.dark) .form-control:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

/* Button */
.submit-btn {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 1rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  position: relative;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(118, 75, 162, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
}

.loading-btn {
  opacity: 0.8;
  cursor: not-allowed;
}

.loader {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-msg {
  color: #ff6b6b;
  font-size: 0.9rem;
  text-align: center;
  background: rgba(255, 107, 107, 0.1);
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 107, 107, 0.2);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
