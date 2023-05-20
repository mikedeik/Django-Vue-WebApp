<template>
  <div>
      <h2>test</h2>
    <ul>
      <li v-for="notification in notifications" :key="notification.id">
        {{ notification.message }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, onMounted, onBeforeUnmount } from 'vue';


export default defineComponent({
  setup() {
    const notifications: any = reactive([]);
    const socketUrl = `ws://localhost:8000/ws/notifications/1/`;
    let socket: WebSocket | null = null;
    const handleNotification = (notification: any) => {
      notifications.push(notification);
    };



    onMounted(() => {

      socket = new WebSocket(
          socketUrl
      );

      if(socket.OPEN){
        console.log("opened connection");
      }
      socket.addEventListener("message", (event) =>{
        console.log("message from server");
        console.log(event.data);
      } )

      socket.onmessage = (event) => {
        console.log("event occured");
        const notification = JSON.parse(event.data);
        handleNotification(notification);
      };

      console.log(socket.readyState);
    });
    onBeforeUnmount(() => {
      if (socket) {
        socket.close();
        console.log("socket closed");
        socket = null;
      }
    });

    return {
      notifications,
    };
  },
});
</script>
