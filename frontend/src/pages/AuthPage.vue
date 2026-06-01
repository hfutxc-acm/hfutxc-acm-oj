<template>
  <div class="auth-root">
    <!-- Neon Rainbow Canvas Background -->
    <div class="neon-bg">
      <!-- Macaron neon blobs -->
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
      <div class="blob blob-4"></div>
      <div class="blob blob-5"></div>
      <div class="blob blob-6"></div>

      <!-- Floating sparkle particles -->
      <div v-for="i in 20" :key="i" class="particle" :style="particleStyle(i)">✦</div>

      <!-- Grid overlay for depth -->
      <div class="grid-overlay"></div>
    </div>

    <!-- Login Card -->
    <div class="card-wrapper">
      <div class="auth-card">
        <!-- Glowing border ring -->
        <div class="card-glow-ring"></div>

        <!-- Header -->
        <div class="card-header">
          <div class="logo-ring">
            <span class="logo-emoji">⚡</span>
          </div>
          <h1 class="card-title">HFUTXC ACM OJ</h1>
          <p class="card-subtitle">面向新手引导 · 系统训练 · 比赛交流</p>
        </div>

        <!-- Tabs -->
        <div class="tab-switcher">
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'login' }"
            @click="activeTab = 'login'; errorMsg = ''"
            id="tab-login"
          >登录</button>
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'register' }"
            @click="activeTab = 'register'; errorMsg = ''"
            id="tab-register"
          >注册</button>
          <div class="tab-indicator" :style="activeTab === 'login' ? 'left:4px' : 'left:calc(50% + 4px)'"></div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="auth-form">
          <div class="field-group">
            <label class="field-label" for="username">用户名</label>
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input
                id="username"
                type="text"
                v-model="form.username"
                placeholder="输入您的用户名"
                class="neon-input"
                required
                autocomplete="username"
              />
            </div>
          </div>

          <div class="field-group">
            <label class="field-label" for="password">密码</label>
            <div class="input-wrapper">
              <span class="input-icon">🔑</span>
              <input
                id="password"
                :type="showPwd ? 'text' : 'password'"
                v-model="form.password"
                placeholder="输入您的密码"
                class="neon-input"
                required
                autocomplete="current-password"
              />
              <button type="button" class="pwd-toggle" @click="showPwd = !showPwd" tabindex="-1">
                {{ showPwd ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <!-- Error message -->
          <transition name="err-fade">
            <div v-if="errorMsg" class="error-banner">
              <span>⚠️</span> {{ errorMsg }}
            </div>
          </transition>

          <!-- Submit button -->
          <button type="submit" class="submit-btn" :disabled="loading" id="btn-submit">
            <span v-if="loading" class="spinner"></span>
            <span v-else class="btn-icon">{{ activeTab === 'login' ? '🚀' : '✨' }}</span>
            {{ loading
              ? (activeTab === 'login' ? '登录中...' : '注册中...')
              : (activeTab === 'login' ? '立即登录' : '注册账号') }}
          </button>
        </form>

        <!-- Footer hint -->
        <p class="card-footer-hint">
          {{ activeTab === 'login' ? '还没有账号？' : '已有账号？' }}
          <button class="switch-link" @click="activeTab = activeTab === 'login' ? 'register' : 'login'">
            {{ activeTab === 'login' ? '立即注册' : '返回登录' }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { navigateTo } from '../router'
import { authApi } from '../api/auth'

const activeTab = ref('login')
const loading = ref(false)
const errorMsg = ref('')
const showPwd = ref(false)

const form = ref({ username: '', password: '' })

function particleStyle(i) {
  const seed = i * 137.5
  return {
    left: `${(seed * 0.618) % 100}%`,
    top: `${(seed * 0.382) % 100}%`,
    animationDelay: `${(i * 0.3) % 6}s`,
    animationDuration: `${4 + (i % 5)}s`,
    fontSize: `${10 + (i % 12)}px`,
    opacity: 0.15 + (i % 5) * 0.07,
    color: ['#ffb3c6','#b5f0ff','#d5b3ff','#b3ffd8','#ffd6b3','#ffe6b3','#c3f0b3'][i % 7],
  }
}

async function handleSubmit() {
  if (!form.value.username || !form.value.password) {
    errorMsg.value = '请填写完整信息'
    return
  }
  errorMsg.value = ''
  loading.value = true
  try {
    const authStore = useAuthStore()
    if (activeTab.value === 'login') {
      const data = await authApi.login(form.value.username, form.value.password)
      authStore.setToken(data.access_token)
      await authStore.initAuth()
      navigateTo('/')
    } else {
      await authApi.register(form.value.username, form.value.password)
      activeTab.value = 'login'
      const data = await authApi.login(form.value.username, form.value.password)
      const authStore = useAuthStore()
      authStore.setToken(data.access_token)
      await authStore.initAuth()
      navigateTo('/')
    }
  } catch (e) {
    errorMsg.value = e.message || '网络错误，请检查服务器连接'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* ─── Root ─── */
.auth-root {
  flex: 1;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  background: #0a0012;
  min-height: 100vh;
}

/* ─── Neon Background ─── */
.neon-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

/* Macaron blobs */
.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
  animation: blobDrift 10s ease-in-out infinite alternate;
}
.blob-1 { width: 520px; height: 520px; background: radial-gradient(circle, #ff8fb3cc, transparent 70%); top: -10%; left: -8%; animation-duration: 12s; }
.blob-2 { width: 420px; height: 420px; background: radial-gradient(circle, #b8f3ffcc, transparent 70%); top: 10%; right: -5%; animation-duration: 9s; animation-delay: -3s; }
.blob-3 { width: 480px; height: 480px; background: radial-gradient(circle, #d4b3ffcc, transparent 70%); bottom: -5%; left: 15%; animation-duration: 14s; animation-delay: -6s; }
.blob-4 { width: 350px; height: 350px; background: radial-gradient(circle, #b3ffd5cc, transparent 70%); bottom: 10%; right: 10%; animation-duration: 11s; animation-delay: -2s; }
.blob-5 { width: 300px; height: 300px; background: radial-gradient(circle, #ffe4b3cc, transparent 70%); top: 40%; left: 40%; animation-duration: 8s; animation-delay: -4s; }
.blob-6 { width: 260px; height: 260px; background: radial-gradient(circle, #ffd6f0cc, transparent 70%); top: 60%; right: 35%; animation-duration: 13s; animation-delay: -1s; }

@keyframes blobDrift {
  0%   { transform: translate(0, 0) scale(1); }
  33%  { transform: translate(30px, -20px) scale(1.08); }
  66%  { transform: translate(-20px, 30px) scale(0.95); }
  100% { transform: translate(15px, 10px) scale(1.04); }
}

/* Grid overlay */
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
  background-size: 44px 44px;
}

/* Floating particles */
.particle {
  position: absolute;
  animation: particleFloat linear infinite;
  user-select: none;
}
@keyframes particleFloat {
  0%   { transform: translateY(0) rotate(0deg); opacity: 0; }
  10%  { opacity: 1; }
  90%  { opacity: 1; }
  100% { transform: translateY(-120px) rotate(360deg); opacity: 0; }
}

/* ─── Card ─── */
.card-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 420px;
  padding: 16px;
}

.auth-card {
  position: relative;
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(28px) saturate(1.8);
  -webkit-backdrop-filter: blur(28px) saturate(1.8);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 24px;
  padding: 36px 32px 28px;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.08) inset,
    0 24px 80px rgba(0,0,0,0.45),
    0 0 60px rgba(200, 100, 255, 0.12);
  overflow: hidden;
}

/* Card top glow ring */
.card-glow-ring {
  position: absolute;
  top: -2px; left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #ff8fb3, #b8f3ff, #d4b3ff, #b3ffd5, transparent);
  border-radius: 99px;
  animation: ringShimmer 3s linear infinite;
}
@keyframes ringShimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

/* ─── Header ─── */
.card-header { text-align: center; margin-bottom: 24px; }

.logo-ring {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px; height: 64px;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(255,143,179,0.3), rgba(184,243,255,0.3), rgba(212,179,255,0.3));
  border: 1.5px solid rgba(255,255,255,0.25);
  margin-bottom: 12px;
  box-shadow: 0 0 24px rgba(200,120,255,0.3);
  animation: logoPulse 3s ease-in-out infinite;
}
@keyframes logoPulse {
  0%, 100% { box-shadow: 0 0 24px rgba(200,120,255,0.3); }
  50%       { box-shadow: 0 0 40px rgba(200,120,255,0.55); }
}
.logo-emoji { font-size: 28px; }

.card-title {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  margin: 0 0 6px;
  background: linear-gradient(90deg, #ff8fb3, #c4a1ff, #76e4ff, #a8ffcf, #ffe4a0);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: rainbowText 5s linear infinite;
}
@keyframes rainbowText {
  0%   { background-position: 0% center; }
  100% { background-position: 300% center; }
}

.card-subtitle {
  color: rgba(255,255,255,0.5);
  font-size: 13px;
  margin: 0;
  letter-spacing: 0.5px;
}

/* ─── Tab Switcher ─── */
.tab-switcher {
  position: relative;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: rgba(255,255,255,0.07);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 24px;
}
.tab-btn {
  position: relative;
  z-index: 1;
  padding: 9px;
  border: none;
  background: transparent;
  color: rgba(255,255,255,0.5);
  font-size: 14px;
  font-weight: 600;
  border-radius: 9px;
  cursor: pointer;
  transition: color 0.25s;
}
.tab-btn.active { color: #fff; }
.tab-indicator {
  position: absolute;
  top: 4px; bottom: 4px;
  width: calc(50% - 4px);
  background: linear-gradient(135deg, rgba(255,143,179,0.4), rgba(212,179,255,0.4));
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 9px;
  transition: left 0.3s cubic-bezier(0.4,0,0.2,1);
  backdrop-filter: blur(6px);
}

/* ─── Form ─── */
.auth-form { display: flex; flex-direction: column; gap: 16px; }

.field-group { display: flex; flex-direction: column; gap: 7px; }

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.7);
  letter-spacing: 0.3px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 13px;
  font-size: 15px;
  pointer-events: none;
  z-index: 1;
}

.neon-input {
  width: 100%;
  padding: 11px 44px 11px 40px;
  background: rgba(255,255,255,0.07);
  border: 1.5px solid rgba(255,255,255,0.15);
  border-radius: 11px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s, background 0.2s;
  font-family: inherit;
  box-sizing: border-box;
}
.neon-input::placeholder { color: rgba(255,255,255,0.3); }
.neon-input:focus {
  border-color: rgba(212,179,255,0.6);
  background: rgba(255,255,255,0.1);
  box-shadow: 0 0 0 3px rgba(212,179,255,0.15), 0 0 16px rgba(212,179,255,0.1);
}

.pwd-toggle {
  position: absolute;
  right: 11px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 2px;
  opacity: 0.6;
  transition: opacity 0.2s;
}
.pwd-toggle:hover { opacity: 1; }

/* ─── Error ─── */
.error-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 80, 100, 0.15);
  border: 1px solid rgba(255, 80, 100, 0.35);
  color: #ffb3b3;
  border-radius: 10px;
  padding: 10px 13px;
  font-size: 13px;
  font-weight: 500;
}
.err-fade-enter-active, .err-fade-leave-active { transition: all 0.25s; }
.err-fade-enter-from, .err-fade-leave-to { opacity: 0; transform: translateY(-6px); }

/* ─── Submit Button ─── */
.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 13px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #ff8fb3, #c084fc, #60cdff, #a7f3b0);
  background-size: 300% 100%;
  color: #1a0030;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.2s, opacity 0.2s;
  animation: btnGradient 4s linear infinite;
  box-shadow: 0 4px 24px rgba(192, 132, 252, 0.4);
  margin-top: 4px;
  font-family: inherit;
}
@keyframes btnGradient {
  0%   { background-position: 0% center; }
  100% { background-position: 300% center; }
}
.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(192, 132, 252, 0.55);
}
.submit-btn:active:not(:disabled) { transform: translateY(0); }
.submit-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-icon { font-size: 16px; }

/* Spinner */
.spinner {
  display: inline-block;
  width: 16px; height: 16px;
  border: 2.5px solid rgba(0,0,0,0.3);
  border-top-color: rgba(0,0,0,0.8);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Footer hint ─── */
.card-footer-hint {
  text-align: center;
  margin-top: 16px;
  font-size: 13px;
  color: rgba(255,255,255,0.4);
}
.switch-link {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: rgba(212,179,255,0.85);
  text-decoration: underline;
  text-underline-offset: 3px;
  padding: 0;
  font-family: inherit;
  transition: color 0.2s;
}
.switch-link:hover { color: #d4b3ff; }
</style>
