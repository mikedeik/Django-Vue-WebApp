<template>
  <div class="pi pi-bell" @click="toggle"></div>
  <div class="count" v-if="notificationsInc.length > 0">{{ notificationsInc.length }}</div>

  <OverlayPanel ref="op">
    <div class="op-container">
      <div v-for="notification in notificationsInc" :key="notification.id" @click="openNotification(notification)">
        <div class="notification">
          <div class="notification-title">
            {{ notification.title }}
          </div>
          <div class="notification-content">
            {{ notification.message }}
          </div>
        </div>
      </div>
    </div>
  </OverlayPanel>
  <Dialog
      v-model:visible="isPoiModalVisible"
      modal
      :header="selectedPoi?.name || 'POI'"
      :style="{ width: '50vw' }"
    >
      <div class="container">
        <div class="image-container">
          <img
            class="image"
            src="https://fastly.picsum.photos/id/949/536/354.jpg?hmac=biBe6mOyyM3zjcsRQcyxfkHTNxHLyMzX2-x9rc-Ef8c"
            alt="Image"
          />
        </div>
        <div class="info-container">
          <div class="top">
            <h1 class="info-row">{{ selectedPoi?.name }}</h1>
            <h3 class="info-row">{{ selectedPoi?.description }}</h3>
            <div class="info-row">
              Coordinates: {{ selectedPoi?.latitude }},{{
                selectedPoi?.longitude
              }}
            </div>
          </div>
          <div class="bottom">

            <div
              :class="selectedPoi?.isFavorite ? 'pi pi-heart-fill' : 'pi pi-heart'"

            ></div>
          </div>
        </div>
      </div>
    </Dialog>
</template>

<script setup lang="ts">

import { useRouter } from "vue-router";
import {onMounted, ref} from "vue";
import OverlayPanel from "primevue/overlaypanel";
import Dialog from "primevue/dialog";
import {PointOfInterest} from "../../Types/PointOfInterest";
import {getPoi} from "../../API/APICalls.vue";

const router = useRouter();
const props = defineProps(['notificationsInc']);
const isPoiModalVisible = ref(false);
const selectedPoi = ref<PointOfInterest>();

const op = ref();
const toggle = (event: unknown) => {
  op.value.toggle(event);
};

const openNotification = async (notification: any) => {
  const response = await getPoi(notification.PoiId);
  if(response.success){
    selectedPoi.value = {
      id: response.PointOfInterestId,
      name: response.Name,
      description: response.Description,
      longitude: response.Longitude,
      latitude: response.Latitude,
      categoryId: response.Categories,
      isFavorite: true,
    };
    isPoiModalVisible.value = true;

  }

}

onMounted(() => {
  console.log('notifications' + props.notificationsInc);
})
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
