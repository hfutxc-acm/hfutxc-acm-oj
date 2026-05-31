<script setup>
import { RecycleScroller } from 'vue-virtual-scroller'
import 'vue-virtual-scroller/dist/vue-virtual-scroller.css'

defineProps({
  rows: { type: Array, default: () => [] }
})
</script>

<template>
  <div class="table-wrap flex flex-col h-[600px] bg-card rounded-md border border-border">
    <!-- Header -->
    <div class="grid grid-cols-7 p-4 border-b border-border bg-muted/50 font-semibold text-sm text-muted-foreground sticky top-0">
      <div>排名</div>
      <div>用户名</div>
      <div>签名</div>
      <div>AC 数</div>
      <div>提交数</div>
      <div>通过率</div>
      <div>最近活跃</div>
    </div>
    
    <!-- Virtual Scroller -->
    <RecycleScroller
      class="flex-1 overflow-y-auto"
      :items="rows"
      :item-size="52"
      key-field="rank"
      v-slot="{ item }"
    >
      <div class="grid grid-cols-7 p-4 border-b border-border text-sm items-center hover:bg-muted/30 transition-colors h-[52px]">
        <div class="font-medium">{{ item.rank }}</div>
        <div>{{ item.username }}</div>
        <div class="truncate pr-2 text-muted-foreground">{{ item.signature }}</div>
        <div>{{ item.ac }}</div>
        <div>{{ item.submissions }}</div>
        <div>{{ item.submissions ? Math.round((item.ac / item.submissions) * 100) : 0 }}%</div>
        <div class="text-xs text-muted-foreground">{{ item.lastActive }}</div>
      </div>
    </RecycleScroller>
  </div>
</template>
