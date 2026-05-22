<script setup>
import { onMounted, ref } from 'vue'
import { getContests } from '../api/contests'
import ContestTable from '../components/contest/ContestTable.vue'

const contests = ref([])

onMounted(async () => {
  contests.value = await getContests()
})
</script>

<template>
  <section class="page-grid">
    <div class="page-heading">
      <p class="eyebrow">Contest</p>
      <h1>比赛</h1>
      <p>校赛、新生赛、周赛、月赛和补题赛。</p>
    </div>
    <ContestTable :contests="contests" />
  </section>
</template>
