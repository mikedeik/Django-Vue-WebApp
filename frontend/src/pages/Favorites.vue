<template>
  <div class="favorites-container">
    <div class="header">
      <Header></Header>
    </div>
    <div class="content">
      <div class="form-container">
        <div class="saved-search-form">
          <label class="label-control" for="latitude">Latitude:</label>
          <input class="form-control" type="number" v-model="lat" id="latitude" />
          <label class="label-control" for="longitude">Longitude:</label>
          <input class="form-control" type="number" v-model="long" id="longitude" />
          <MultiSelect
            class="multi-select"
            v-model="selectedCategories"
            display="chip"
            :options="categories"
            optionLabel="name"
            placeholder="Κατηγορίες"
          />
          <label class="label-control" for="radius">Radius (km):</label>
          <input class="form-control" type="number" v-model="radius" id="radius" />
          <button @click="CreateSearch" class="btn btn-primary mb-2">
            Add to favorites
          </button>
        </div>
    </div>

      <div class="map-container" ref="mapContainer" />
    </div>


  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import Header from "../components/common/Header.vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import MultiSelect from "primevue/multiselect";
import {getCategories, CreateSavedSearch} from "../API/APICalls.vue";
import {Category} from "../Types/Category";

export default defineComponent({


  components: {MultiSelect, Header},
  setup() {
    const categories = ref<Category[]> ([]);
    const selectedCategories = ref<Category[]> ([]);
    const mapContainer = ref<HTMLDivElement | null>(null);
    const long = ref(23.78);
    const lat = ref(37.98);
    const radius = ref(10);
    const currMarker = ref<L.Marker>();
    let map: any;
    let circle: any;
    onMounted(() => {
      map = L.map(mapContainer.value).setView([lat.value, long.value], 13);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
      }).addTo(map);
      drawMarker(lat.value, long.value, radius.value, map);

      getCategories().then((res) => {
        if(res.success){
          res.map((category : any) => {
            categories.value.push({
              value: category.CategoryId,
              name: category.Name
            })
          })
        }
        else{
          alert(res.error);
        }
      }).catch()

    });
    watch([lat, long, radius], () => {
      deleteMarker(currMarker.value, map, circle);
      drawMarker(lat.value, long.value, radius.value, map);
    });

    function drawMarker(lat, long, radius, map) {
      currMarker.value = L.marker([lat, long]);
      currMarker.value.addTo(map).bindPopup("Your Location");
      circle = L.circleMarker([lat, long], {
        radius: radius * 10,
      }).addTo(map);
      map.setView([lat, long], 13);
    }
    function deleteMarker(marker, map, circle) {
      map.removeLayer(marker);
      map.removeLayer(circle);
    }
    const  CreateSearch = async () => {
      //TODO
      console.log("clicked");
      let data = {
        CenterLatitude: lat.value,
        CenterLongitude: long.value,
        Radius: radius.value, //in km
        Categories: selectedCategories.value.map((c)=>{
          return c.value
        })
      };
      console.log(data);
      CreateSavedSearch(data).catch((e) => console.error(e));

    }

    return {
      mapContainer,
      lat,
      long,
      radius,
      categories,
      selectedCategories,
      CreateSearch
    };
  },
});
</script>

<style scoped>

.header {
  height: 10%;
}

.form-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.saved-search-form {
  display: flex;
  flex-direction: column;
  height: 90%;
  width: 50%;
  border: solid;
  border-width: 2px;
  border-radius: 10px;
  margin: 10px;
  align-items: flex-start;
  justify-content: center;
}

.multi-select{
  margin: 20px;
  max-width: 90%;
}

.map-container {
  width: 100%;
  height: 80vh; /* Adjust the height as needed */
  color: #cccccc;
}

.mb-2 {
  margin : 20px;
}
.form-control {
  width: 70%;
  margin : 0px 20px 0px 20px;
}
.label-control {
  margin : 0px 20px 0px 20px;
}
.content {
  display: grid;
  grid-template-columns: 2fr 2fr; /* Adjust the column widths as needed */
  gap: 20px; /* Adjust the gap between columns as needed */
  height: 80vh; /* Adjust the height as needed */
}
</style>
