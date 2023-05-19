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
    let socket: WebSocket | null = null;

    const handleNotification = (event: MessageEvent) => {
      const notification = JSON.parse(event.data);
      notifications.push(notification);
    };

    onMounted(() => {
      const socketUrl = `ws://localhost:8000/ws/notifications/1/`; // Update the URL with the correct ID
      socket = new WebSocket(socketUrl);
      socket.addEventListener('message', handleNotification);
    });

    onBeforeUnmount(() => {
      if (socket) {
        socket.close();
        socket = null;
      }
    });

    return {
      notifications,
    };
  },
});
</script>
