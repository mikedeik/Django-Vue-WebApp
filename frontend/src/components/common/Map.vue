<template>
  <div class="map-container" ref="mapContainer"></div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, getCurrentInstance, watch } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { PointOfInterest } from "../../Types/PointOfInterest";

export default defineComponent({
  props: {
    pointsOfInterest: {
      type: Array as () => PointOfInterest[],
      required: true,
    },
  },
  setup(props) {
    const mapContainer = ref(null);
    const instance = getCurrentInstance();
    let map :any;

    // Create a watcher for the pointsOfInterest prop
    watch(
      () => props.pointsOfInterest,
      (newPointsOfInterest) => {
        // Perform any necessary actions to update the map with the new pointsOfInterest
        updateMapMarkers(newPointsOfInterest);
      }
    );

    onMounted(() => {
      map = L.map(mapContainer.value).fitBounds(
        getBounds(props.pointsOfInterest)
      );

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
          'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
      }).addTo(map);

      // Create markers for the initial pointsOfInterest
      updateMapMarkers(props.pointsOfInterest);
    });

    // Helper function to calculate the bounds of all points
    function getBounds(points: PointOfInterest[]) {
      const latLngs = points.map((poi) =>
        L.latLng(poi.latitude, poi.longitude)
      );
      return L.latLngBounds(latLngs);
    }

    // Helper function to update the map markers
    function updateMapMarkers(pointsOfInterest: PointOfInterest[]) {
      // Clear existing markers
      map.eachLayer((layer: any) => {
        if (layer instanceof L.Marker) {
          map.removeLayer(layer);
        }
      });

      // Create new markers based on the updated pointsOfInterest
      pointsOfInterest.forEach((poi) => {
        L.marker([poi.latitude, poi.longitude])
          .addTo(map)
          .bindPopup(`<strong>${poi.name}</strong><br>${poi.description}`)
          .on("click", () => instance?.emit("clickedPoi", poi));
      });
    }

    return {
      mapContainer,
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
