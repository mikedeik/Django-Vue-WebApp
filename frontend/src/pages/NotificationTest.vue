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
import io from 'socket.io-client';

export default defineComponent({
  setup() {
    const notifications: any = reactive([]);
    let socket: any = null;

    const handleNotification = (notification: any) => {
      notifications.push(notification);
    };

    onMounted(() => {
      const socketUrl = `ws://localhost:8000/ws/notifications`;
      console.log(socketUrl);
      socket = io(socketUrl, {
        query: {
          id: 1,
        },
      });
      socket.on('notification', handleNotification);
    });

    onBeforeUnmount(() => {
      if (socket) {
        socket.disconnect();
        socket = null;
      }
    });

    return {
      notifications,
    };
  },
});
</script>
