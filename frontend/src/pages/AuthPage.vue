<template>
  <div class="min-h-screen w-full flex items-center justify-center bg-background relative overflow-hidden">
    <!-- Animated Background Shapes -->
    <div class="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-primary/20 blur-[120px] animate-pulse"></div>
    <div class="absolute top-[60%] -right-[10%] w-[40%] h-[60%] rounded-full bg-primary/20 blur-[100px] animate-pulse" style="animation-delay: 2s"></div>

    <Card class="w-full max-w-md relative z-10 border-border/50 shadow-2xl backdrop-blur-sm bg-card/95 mx-4">
      <CardHeader class="space-y-3 text-center pb-6">
        <div class="mx-auto bg-primary/10 w-16 h-16 rounded-2xl flex items-center justify-center mb-2">
          <img src="https://upload.wikimedia.org/wikipedia/zh/e/e8/Icpc_logo.png" alt="ICPC Logo" class="w-10 h-10 object-contain" />
        </div>
        <CardTitle class="text-2xl font-bold tracking-tight">HFUTXC ACM OJ</CardTitle>
        <CardDescription>
          面向新手引导、系统训练、比赛交流与梯队建设
        </CardDescription>
      </CardHeader>

      <CardContent>
        <Tabs v-model="activeTab" class="w-full">
          <TabsList class="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="login">登录</TabsTrigger>
            <TabsTrigger value="register">注册</TabsTrigger>
          </TabsList>
          
          <div v-auto-animate>
            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div class="space-y-2">
                <Label htmlFor="username">用户名</Label>
                <Input 
                  id="username" 
                  type="text" 
                  v-model="form.username" 
                  placeholder="输入您的用户名" 
                  required 
                />
              </div>
              <div class="space-y-2">
                <Label htmlFor="password">密码</Label>
                <Input 
                  id="password" 
                  type="password" 
                  v-model="form.password" 
                  placeholder="输入您的密码" 
                  required 
                />
              </div>

              <div v-if="errorMsg" class="text-sm font-medium text-destructive mt-2 bg-destructive/10 p-3 rounded-md">
                {{ errorMsg }}
              </div>

              <Button type="submit" class="w-full mt-4" :disabled="loading">
                <span v-if="loading" class="mr-2 animate-spin">⚪</span>
                {{ loading ? (activeTab === 'login' ? '登录中...' : '注册中...') : (activeTab === 'login' ? '立即登录' : '注册账号') }}
              </Button>
            </form>
          </div>
        </Tabs>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { navigateTo } from '../router'
import { authApi } from '../api/auth'
import { vAutoAnimate } from '@formkit/auto-animate/vue'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'

const activeTab = ref('login')
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
    const authStore = useAuthStore()
    if (activeTab.value === 'login') {
      const data = await authApi.login(form.value.username, form.value.password)
      authStore.setToken(data.access_token)
      await authStore.initAuth()
      navigateTo('/')
    } else {
      await authApi.register(form.value.username, form.value.password)
      activeTab.value = 'login'
      await handleSubmit() // auto login
    }
  } catch (e) {
    errorMsg.value = e.message || "网络错误，请检查服务器连接"
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 避免覆盖原本全局样式，完全依赖 Tailwind CSS v3 与 shadcn */
</style>
