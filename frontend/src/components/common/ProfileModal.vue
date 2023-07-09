<template>
  <div class="container" @click="toggle">
    <div class="pi pi-user"></div>
    <div class="pi pi-bars"></div>
  </div>

  <OverlayPanel ref="op">
    <div class="op-container">
      <template v-for="option in displayedOptions" :key="option">
        <div class="option" @click="handleClick(option)">
          {{ option.text }}
        </div>
      </template>
    </div>
  </OverlayPanel>
</template>

<script setup lang="ts">
import OverlayPanel from "primevue/overlaypanel";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const op = ref();

const handleClick = (option: any) => {
  console.log(option);
  if (option.text === "Logout") {
    localStorage.clear();
    console.log("tokens deleted");
    router.push({ path: "pois" });
  } else {
    router.push({ path: option.route });
  }
};

const toggle = (event: unknown) => {
  op.value.toggle(event);
};

//TODO user logged in functionality
const isGuest = ref(false);

const guestOptions = [
  {
    text: "Log In",
    route: "/login",
  },
  {
    text: "Favorites",
    route: "/favorites",
  },
];
const userOptions = [
  {
    text: "Το Προφίλ μου",
    route: "/profile",
  },
  {
    text: "Δημιουργία Αναζήτησης",
    route: "/createsearch",
  },
  {
    text: "Αγαπημένα",
    route: "/favorites",
  },
  {
    text: "Logout",
    route: "/home", //todo logout user and redirect to home
  },
];

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
