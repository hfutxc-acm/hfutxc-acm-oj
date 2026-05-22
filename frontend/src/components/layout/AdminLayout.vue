<script setup>
import AppSidebar from './AppSidebar.vue'
</script>

<template>
  <div class="admin-layout">
    <AppSidebar />
    <section class="admin-content">
      <slot />
    </section>
  </div>
</template>
