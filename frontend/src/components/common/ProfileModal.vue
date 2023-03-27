<template>
  <div class="container" @click="toggle">
    <div class="pi pi-user"></div>
    <div class="pi pi-bars"></div>
  </div>

  <OverlayPanel ref="op">
    <div class="op-container">
      <template v-for="option in displayedOptions" :key="option">
        <div class="option">{{ option }}</div>
      </template>
    </div>
  </OverlayPanel>
</template>

<script setup lang="ts">
import OverlayPanel from "primevue/overlaypanel";
import { computed, ref } from "vue";

const op = ref();
const toggle = (event: unknown) => {
  op.value.toggle(event);
};

//TODO user logged in functionality
const isGuest = ref(false);

const guestOptions = ["Log In/Sign Up", "FAQ"];
const userOptions = ["My Profile", "Favorites", "FAQ", "Logout"];

const displayedOptions = computed(() => {
  if (isGuest.value) {
    return guestOptions;
  } else {
    return userOptions;
  }
});
</script>

<style scoped lang="scss">
.container {
  width: 88px;
  height: 48px;
  border: 1px solid gray;
  border-radius: 100px;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  cursor: pointer;
}
.pi-bars {
  color: gray;
  font-size: 18px;
}
.op-container {
  width: 140px;
}
.option {
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  color: gray;
  padding: 4px;
  &:hover {
    color: black;
  }
}
</style>
