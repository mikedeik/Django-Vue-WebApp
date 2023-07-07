<template>
  <div class="favorites-container">
    <div class="header">
      <Header></Header>
    </div>
    <div class="map-container" ref="mapContainer" />
    <div>
      <label for="latitude">Latitude:</label>
      <input class="form-control" type="number" v-model="lat" id="latitude" />

      <label for="longitude">Longitude:</label>
      <input class="form-control" type="number" v-model="long" id="longitude" />

      <label for="radius">Radius (km):</label>
      <input class="form-control" type="number" v-model="radius" id="radius" />
    </div>
    <button type="submit" @click="onSubmit" class="btn btn-primary mb-2">
      Add to favorites
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default defineComponent({
  setup() {
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
    }
    function deleteMarker(marker, map, circle) {
      map.removeLayer(marker);
      map.removeLayer(circle);
    }
    function onSubmit() {
      //TODO
    }

    return {
      mapContainer,
      lat,
      long,
      radius,
    };
  },
});
</script>

<style scoped>
.map-container {
  width: 80%;
  height: 80vh; /* Adjust the height as needed */
  color: #cccccc;
}
</style>
