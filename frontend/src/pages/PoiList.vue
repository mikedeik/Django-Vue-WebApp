<template>
  <div class="root">
    <Header/>
    <div class="homepage">
  <div>
    <h2>PoiList</h2>
      <CustomCard v-for="poi in mockPoints" :key="poi.id" :poi="poi" />

    </div>
    <div class="map-container">
      <Map :points-of-interest="mockPoints" key="map" />
    </div>
</div>

  </div>

</template>

<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import Header from "../components/common/Header.vue";
import InputText from 'primevue/inputtext';
import MultiSelect from 'primevue/multiselect';
import {useRouter} from "vue-router";
import axios from "axios";
import Map from "../components/common/Map.vue";
import {PointOfInterest} from '../Types/PointOfInterest';
import CustomCard from "../components/CustomCard/CustomCard.vue";

interface Poi {
  name: string;
  CategoryId: number;
  // Add other properties here if necessary
}
const mockPoints: PointOfInterest[] = [
  {
    id: 1,
    name: 'Point of Interest 1',
          description: 'Description 1',
          longitude: 23.737539,
          latitude: 37.983810,
          image: 'https://fastly.picsum.photos/id/949/536/354.jpg?hmac=biBe6mOyyM3zjcsRQcyxfkHTNxHLyMzX2-x9rc-Ef8c',
          categoryId: 1,
        },
        {
          id: 2,
          name: 'Point of Interest 2',
          description: 'Description 2',
          longitude: 23.787432,
          latitude: 37.983720,
          image: 'https://fastly.picsum.photos/id/886/200/200.jpg?hmac=pfmGQi7EpajLoJI0tKTPTUwOPQtH9YwE-wNl_kr7ErI',
          categoryId: 2,
        },
        {
          id: 3,
          name: 'Point of Interest 3',
          description: 'Description 3',
          longitude: 23.287432,
          latitude: 37.483720,
          image: 'https://fastly.picsum.photos/id/886/200/200.jpg?hmac=pfmGQi7EpajLoJI0tKTPTUwOPQtH9YwE-wNl_kr7ErI',
          categoryId: 2,
        },
]


let pois: any = ref([]);
const new_pois = ref<Poi[]>([]);

onMounted(async () => {
try {
    const response = await axios.get('http://localhost:8000/ecoquest/poi/');
    pois.value = response.data;
    console.log(pois.value);
  } catch (error) {
    console.error(error);
    alert(error);
  }
  console.log(pois.value)
})


</script>

<style scoped lang="scss">
.homepage{
  display: grid;
  grid-template-columns: 2fr 2fr; /* Adjust the column widths as needed */
  gap: 20px; /* Adjust the gap between columns as needed */
  height: 80vh; /* Adjust the height as needed */
}


.map-container {
  width: 100%;
  height: 100%;
}
.poi-list {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.p-datatable{
  height: 100px;
  width: 200px;
}

.poi{
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