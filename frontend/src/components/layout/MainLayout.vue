<script setup>
import AppFooter from './AppFooter.vue'
import AppHeader from './AppHeader.vue'

const props = defineProps({
  authMode: { type: Boolean, default: false }
})
</script>

<template>
  <div class="layout-shell" :class="{ 'auth-mode': authMode }">
    <AppHeader v-if="!authMode" />
    <main class="page-shell" :class="{ 'auth-shell': authMode }">
      <slot />
    </main>
    <AppFooter v-if="!authMode" />
  </div>
</template>
