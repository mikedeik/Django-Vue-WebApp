<template>
  <div class="root">
    <Header />

    <div class="homepage" v-if="typedPois.length">
      <div class="sidebar">
        <Paginator
          :rows="rows"
          :totalRecords="totalCount"
          :rowsPerPageOptions="[10, 20, 30]"
          @page="updatePage"
        ></Paginator>
        <h2>Περιοχές Ενδιαφέροντος</h2>
        <div class="poi-list">
          <CustomCard
            v-for="poi in typedPois"
            :key="poi.id"
            :poi="poi"
            @click="onPoiClick(poi)"
          />
        </div>
      </div>
      <div class="map-container">
        <Map
          :points-of-interest="typedPois"
          key="map"
          @clickedPoi="onPoiClick"
        />
      </div>
    </div>
    <div v-else>No Data to display</div>
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
            <!-- TODO change isFavorite to selectedPoi?.isFavorite -->
            <div
              :class="isFavorite ? 'pi pi-heart-fill' : 'pi pi-heart'"
              @click="onFavorite(selectedPoi)"
            ></div>
          </div>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import Paginator from "primevue/paginator";
import Header from "../components/common/Header.vue";
import Dialog from "primevue/dialog";
import axios from "axios";
import Map from "../components/common/Map.vue";
import { PointOfInterest } from "../Types/PointOfInterest";
import CustomCard from "../components/CustomCard/CustomCard.vue";
import {addToFavorites} from "../API/APICalls.vue";

let pois: any = ref([]);
const rows = ref<number>(10);
const page = ref<number>(1);

const typedPois = ref<PointOfInterest[]>([]);
const totalCount = ref<number>(typedPois.value.length);
const isPoiModalVisible = ref(false);
const selectedPoi = ref<PointOfInterest>();
const isFavorite = ref(false);
const updatePage = (newPage: any) => {
  console.log(newPage);
  page.value = newPage.page + 1;
};

onMounted(async () => {
  try {
    const response = await axios.get(
      "http://localhost:8000/ecoquest/favorites/");

    pois.value = response.data;
  } catch (error) {
    alert(error);
  }

  pois.value.map((poi: any) => {
    typedPois.value.push({
      id: poi.PointOfInterestId,
      name: poi.Name,
      description: poi.Description,
      longitude: poi.Longitude,
      latitude: poi.Latitude,
      categoryId: poi.Categories,
    });
  });
  totalCount.value = typedPois.value.length;
  console.log(pois.value);
});

async function onFavorite (poi: PointOfInterest) {
  console.log("poi", poi);

  //TODO add api call to backend to change favorite to true
  if(!isFavorite.value){
    const response = await addToFavorites(poi.id, true);
    if(response.success){
       isFavorite.value = !isFavorite.value;
    }
    else {
      alert(response.message);
    }
  }
  else {
     const response = await addToFavorites(poi.id, false);
      if(response.success){
        isFavorite.value = !isFavorite.value;
      }
    else {
      alert(response.message);
  }
}
// function onPoiClick(poi: PointOfInterest) {
//   selectedPoi.value = poi;
//   isPoiModalVisible.value = true;
}

</script>

<style scoped lang="scss">
.homepage {
  display: grid;
  grid-template-columns: 2fr 2fr; /* Adjust the column widths as needed */
  gap: 20px; /* Adjust the gap between columns as needed */
  height: 80vh; /* Adjust the height as needed */
}

.map-container {
  width: 100%;
  height: 100%;
  max-height: 100vh;
  color: #4caf50;
}
.sidebar {
  height: 100%;
  overflow-y: scroll;
  padding: 16px;
}
.search-bar {
  padding-bottom: 20px;
}
.poi-list {
  margin-bottom: 20px;
}

.p-datatable {
  height: 100px;
  width: 200px;
}

.poi {
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  color: gray;
  padding: 4px;
  &:hover {
    color: black;
  }
}

.container {
  display: flex;
}

.image-container {
  flex: 1;
}

.image {
  width: 100%;
  height: auto;
}

.info-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.top {
  display: flex;
  flex-direction: column;
  padding-left: 20px;
}
.bottom {
  display: flex;
  justify-content: end;
}
.info-row {
  margin-bottom: 10px;
}
.pi-heart {
  font-size: 32px;
}

.pi-heart-fill {
  font-size: 32px;
  color: red;
}
</style>
