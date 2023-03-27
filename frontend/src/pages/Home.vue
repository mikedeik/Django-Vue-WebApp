<template>
  <div class="home-container">
    <div class="header">
      <Header></Header>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "../components/common/Header.vue";
</script>

<style scoped lang="scss">
.home-container {
  width: 100%;
  height: 100%;
}

.header {
  width: 100%;
  height: 10%;
}
</style>
