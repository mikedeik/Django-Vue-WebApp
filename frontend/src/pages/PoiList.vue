<template>
  <div class="root">
    <Header />
    <div class="search-bar">
      <SearchBar/>
    </div>

    <div class="homepage" v-if="typedPois.length">
      <div class="sidebar">
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
        <Map :points-of-interest="typedPois" key="map" @clickedPoi="onPoiClick" />
      </div>
    </div>
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
          <h1 class="info-row">{{ selectedPoi?.name }}</h1>
          <h3 class="info-row">{{ selectedPoi?.description }}</h3>
          <div class="info-row">
            Coordinates: {{ selectedPoi?.latitude }},{{
              selectedPoi?.longitude
            }}
          </div>
        </div>
      </div>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Header from "../components/common/Header.vue";
import Dialog from "primevue/dialog";
import axios from "axios";
import Map from "../components/common/Map.vue";
import { PointOfInterest } from "../Types/PointOfInterest";
import CustomCard from "../components/CustomCard/CustomCard.vue";
import SearchBar from "../components/common/SearchBar.vue";



let pois: any = ref([]);
const typedPois = ref<PointOfInterest[]>([]);
const isPoiModalVisible = ref(false);
const selectedPoi = ref<PointOfInterest>();

onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:8000/ecoquest/poi/");
    pois.value = response.data;
    console.log(pois.value);
  } catch (error) {
    console.error(error);
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
    })
  })

  console.log(pois.value);
});

function onPoiClick(poi: PointOfInterest) {
  selectedPoi.value = poi;
  isPoiModalVisible.value = true;
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
.search-bar{
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
  // justify-content: space-between;
  padding-left: 20px;
}

.info-row {
  margin-bottom: 10px;
}
</style>
