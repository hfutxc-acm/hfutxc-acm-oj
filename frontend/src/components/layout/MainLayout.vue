<script setup>
import AppFooter from './AppFooter.vue'
import AppHeader from './AppHeader.vue'
</script>

<template>
  <div class="layout-shell">
    <AppHeader />
    <main class="page-shell">
      <slot />
    </main>
    <AppFooter />
  </div>
</template>
