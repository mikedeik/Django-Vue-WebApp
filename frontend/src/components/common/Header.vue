<template>
  <div class="header-container">
    <div class="logo">
      <Logo />
    </div>
    <div class="title">Explore Nature Like Never Before</div>
    <div class="np-pair">
      <div class="notification"><Notification /></div>
      <div class="profile-options"><ProfileModal  /></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Logo from "./Logo.vue";
import ProfileModal from "./ProfileModal.vue";
import Notification from "./Notification.vue";
</script>

<style scoped lang="scss">
.header-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
  color: #75c027;
  font-size: 28px;
  font-weight: bold;
}
.np-pair {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 140px;
}
</style>
