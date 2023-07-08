<template>
  <div class="header-container">
    <div class="logo">
      <Logo />
    </div>
    <div class="title">Explore Nature Like Never Before</div>
    <div v-if="isLogged" class="np-pair">
      <div class="notification"><Notification /></div>
      <div class="profile-options"><ProfileModal /></div>
    </div>
    <div v-if="!isLogged" class="button-container">
      <div class="login-button">
        <Button @click="handleClick"> Σύνδεση </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Logo from "./Logo.vue";
import ProfileModal from "./ProfileModal.vue";
import Notification from "./Notification.vue";
import { NotificationType } from "../../Types/Notification";
import { useRouter } from "vue-router";
import {onBeforeUnmount, onMounted, reactive, ref} from "vue";

const isLogged = ref(false);
const notifications = ref<NotificationType[]>([]);
let socket: WebSocket | null = null;

const router = useRouter();
const handleClick = () => {
  router.push({ path: "login" });
};

const handleNotification = (notification: NotificationType) => {
  notifications.value.push(notification);
}

onMounted(() => {
  const token:string | null = localStorage.getItem("refreshToken");

  if (token !== undefined && token !== "" && token !== null) {
    isLogged.value = true;
  } else {
    isLogged.value = false;
  }

  const user_id = localStorage.getItem("user_id");
  if(user_id){
    const socketUrl = `ws://localhost:8000/ws/notifications/${user_id}/`;
    socket = new WebSocket(
        socketUrl
    );

    if(socket.OPEN){
        console.log("opened connection");
        console.log(socket.url)
    }
    socket.addEventListener("message", (event) =>{
        console.log("message from server");
        console.log(event.data);
        const notification = JSON.parse(event.data);
        handleNotification(notification);
    });
  }

});

onBeforeUnmount(() => {
      if (socket) {
        socket.close();
        console.log("socket closed");
        socket = null;
      }
    });
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
.button-container {
  padding: 10px;
}
.login-button {
  background-color: #75c027;
  padding: 5px;
  border-radius: 5px;
  width: 100px;
  height: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.np-pair {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 140px;
}
</style>
