<template>
  <div class="logo" @click="router.push('/home')">
    <img :src="Logo" />
  </div>
</template>

<script setup lang="ts">
import Logo from "../../assets/logo.png";
import { useRouter } from "vue-router";

const router = useRouter();
</script>

<style scoped lang="scss">
.logo {
  cursor: pointer;
}
</style>
