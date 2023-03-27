<template>
  <div class="pi pi-bell" @click="toggle"></div>
  <div class="count" v-if="notificationCount > 0">{{ notificationCount }}</div>

  <OverlayPanel ref="op">
    <div class="op-container">
      <template v-for="notification in notifications" :key="notification">
        <div class="notification">
          <div class="notification-title">
            {{ notification.title }}
          </div>
          <div class="notification-content">
            {{ notification.content }}
          </div>
        </div>
      </template>
    </div>
  </OverlayPanel>
</template>

<script setup lang="ts">
import Logo from "../../assets/logo.png";
import { useRouter } from "vue-router";
import { ref } from "vue";
import OverlayPanel from "primevue/overlaypanel";

const router = useRouter();
//TODO fix
const notificationCount = ref(2);

const notifications = ref([
  {
    title: "New POI in Athens",
    content: " POI added in your search",
  },
  {
    title: "New POI in Syros",
    content: " POI added in your search",
  },
]);
const op = ref();
const toggle = (event: unknown) => {
  op.value.toggle(event);
};
</script>

<style scoped lang="scss">
.pi-bell {
  font-size: 24px;
  color: gray;
}
.count {
  position: absolute;
  top: 30px;
  right: 110px;
  width: 20px;
  height: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 25px;
  background-color: red;
  font-weight: 700;
  color: white;
}
.op-container {
  width: 320px;
  max-height: 600px;
  overflow: auto;
  padding: 4px;
}
.notification {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-evenly;
  height: 60px;
  border-bottom: 1px solid black;
  cursor: pointer;
  &:hover {
    background-color: #75c02750;
  }

  &-title {
    font-weight: 600;
    width: 100%;
    height: 20px;
  }
}
</style>
