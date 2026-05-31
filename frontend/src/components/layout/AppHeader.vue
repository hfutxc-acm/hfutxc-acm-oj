<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { currentRoute, navigateTo } from '../../router'
import { useAuthStore } from '../../stores/authStore'
import { useThemeStore } from '../../stores/themeStore'
import { vAutoAnimate } from '@formkit/auto-animate/vue'

import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Moon, Sun, Palette, LogOut, User as UserIcon, LayoutDashboard } from 'lucide-vue-next'

const navItems = [
  { label: '首页', path: '/' },
  { label: '题库', path: '/problems' },
  { label: '训练', path: '/trainings' },
  { label: '比赛', path: '/contests' },
  { label: '发布题解', path: '/solutions/publish' },
  { label: '排行', path: '/rankings' },
  { label: '团队', path: '/teams' },
  { label: '知识库', path: '/wiki/', external: true }
]

const showColorPicker = ref(false)
const colors = [
    { name: "red", hex: "#ff8787" },
    { name: "pink", hex: "#fcc2d7" },
    { name: "purple", hex: "#e599f7" },
    { name: "deep-purple", hex: "#b197fc" },
    { name: "indigo", hex: "#91a7ff" },
    { name: "blue", hex: "#74c0fc" },
    { name: "light-blue", hex: "#66d9e8" },
    { name: "cyan", hex: "#63e6be" },
    { name: "teal", hex: "#38d9a9" },
    { name: "green", hex: "#8ce99a" },
    { name: "light-green", hex: "#b2f2bb" },
    { name: "lime", hex: "#d8f5a2" },
    { name: "yellow", hex: "#ffec99" },
    { name: "amber", hex: "#ffe066" },
    { name: "orange", hex: "#ffd43b" },
    { name: "rainbow", hex: "linear-gradient(to right, #ff6b6b, #ffb347, #ffeb3b, #77dd77, #4dd0e1, #64b5f6, #ba68c8)", isRainbow: true },
    { name: "brown", hex: "#e6ca90" },
    { name: "grey", hex: "#ced4da" },
    { name: "blue-grey", hex: "#a5d8ff" },
    { name: "black", hex: "#868e96" }
]

function selectColor(c) {
    localStorage.setItem("custom-primary-color", c.name)
    document.documentElement.setAttribute("data-primary-color", c.name)
    showColorPicker.value = false
}

function handleNavClick(item) {
  if (item.external) {
    window.location.href = item.path
  } else {
    navigateTo(item.path)
  }
}

function isActive(path) {
  if (path === '/') return currentRoute.value.name === 'home'
  return currentRoute.value.name?.startsWith(path.slice(1).split('/')[0])
}

const closePicker = () => {
    showColorPicker.value = false
}

onMounted(() => {
    document.addEventListener('click', closePicker)
})
onUnmounted(() => {
    document.removeEventListener('click', closePicker)
})
</script>

<template>
  <header class="app-header">
    <button class="brand" @click="navigateTo('/')">
      <strong>HFUTXC ACM</strong>
      <span>Online Judge</span>
    </button>
    <nav class="main-nav" v-auto-animate>
      <template v-for="item in navItems" :key="item.path">
        <button
          :class="{ active: isActive(item.path) }"
          @click="handleNavClick(item)"
        >
          {{ item.label }}
        </button>
      </template>
    </nav>
    <div class="header-actions flex items-center gap-3" v-auto-animate>
      <!-- Dark/Light Mode toggle -->
      <Button variant="ghost" size="icon" @click="useThemeStore().toggleTheme()" title="切换深色/浅色模式">
        <Sun v-if="useThemeStore().currentTheme === 'dark'" class="w-5 h-5" />
        <Moon v-else class="w-5 h-5" />
      </Button>

      <!-- Color Picker -->
      <div class="color-picker-wrapper" @click.stop>
        <Button variant="ghost" size="icon" @click="showColorPicker = !showColorPicker" title="主题色">
          <Palette class="w-5 h-5" />
        </Button>
        <div v-if="showColorPicker" class="color-palette-popover">
            <div class="color-grid">
                <button v-for="c in colors" :key="c.name" 
                    class="color-swatch"
                    :class="{'is-rainbow': c.isRainbow}"
                    :style="c.isRainbow ? { background: c.hex } : { backgroundColor: c.hex }"
                    @click="selectColor(c)"
                    :title="c.name">
                </button>
            </div>
        </div>
      </div>

      <!-- Auth Actions -->
      <div v-if="useAuthStore().isAuthenticated" class="ml-2">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" class="relative h-8 w-8 rounded-full">
              <Avatar class="h-8 w-8">
                <AvatarImage src="" alt="@user" />
                <AvatarFallback>{{ useAuthStore().currentUser?.username?.charAt(0)?.toUpperCase() || 'U' }}</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent class="w-56" align="end">
            <DropdownMenuLabel class="font-normal flex flex-col space-y-1">
              <p class="text-sm font-medium leading-none">{{ useAuthStore().currentUser?.username }}</p>
              <p class="text-xs leading-none text-muted-foreground">{{ useAuthStore().currentUser?.role }}</p>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="navigateTo('/me')">
              <UserIcon class="mr-2 h-4 w-4" />
              <span>个人中心</span>
            </DropdownMenuItem>
            <DropdownMenuItem v-if="useAuthStore().canAccessAdmin" @click="navigateTo('/admin')">
              <LayoutDashboard class="mr-2 h-4 w-4" />
              <span>管理后台</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="useAuthStore().logout()">
              <LogOut class="mr-2 h-4 w-4" />
              <span>退出登录</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div v-else class="ml-2">
        <Button variant="secondary" size="sm" @click="navigateTo('/auth')" class="font-semibold text-primary-dark">
          登录 / 注册
        </Button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 20px;
  align-items: center;
  padding: 14px 28px;
  background: var(--primary);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
}

.brand {
  display: grid;
  gap: 1px;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--primary-dark);
  text-align: left;
  cursor: pointer;
}

.brand strong {
  font-size: 18px;
}

.brand span {
  color: var(--header-text-dim, var(--muted));
  font-size: 12px;
}

.main-nav {
  display: flex;
  gap: 6px;
  justify-content: center;
  overflow-x: auto;
}

.main-nav button {
  min-height: 38px;
  padding: 0 13px;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: var(--header-text-muted, rgba(255, 255, 255, 0.8));
  cursor: pointer;
  font-weight: 700;
  white-space: nowrap;
  transition: all 0.2s;
}

.main-nav button.active,
.main-nav button:hover {
  background: var(--header-btn-bg-hover, rgba(0, 0, 0, 0.1));
  color: var(--header-text, #ffffff);
}

.color-picker-wrapper {
    position: relative;
}

.color-palette-popover {
    position: absolute;
    top: 120%;
    right: 0;
    width: 220px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    z-index: 100;
    animation: pop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes pop {
    0% { opacity: 0; transform: translateY(-10px) scale(0.95); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}

.color-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
}

.color-swatch {
    width: 100%;
    aspect-ratio: 1;
    border-radius: 50%;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.2s;
}

.color-swatch:hover {
    transform: scale(1.15);
    border-color: var(--text);
}

.is-rainbow {
    animation: rotate-bg 3s linear infinite;
}

@keyframes rotate-bg {
    100% { filter: hue-rotate(360deg); }
}
</style>
