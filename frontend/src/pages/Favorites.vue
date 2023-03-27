<template>
  <div class="favorites-container">
    <div class="header">
      <Header></Header>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "../components/common/Header.vue";
</script>

<style scoped lang="scss">
.favorites-container {
  width: 100%;
  height: 100%;
}

.header {
  height: 10%;
  width: 100%;
}
</style>
