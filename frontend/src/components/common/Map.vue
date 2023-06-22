<template>
    <div class="map-container" ref="mapContainer"></div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';
  import { PointOfInterest } from '../../Types/PointOfInterest';
  
  export default defineComponent({
    props: {
      pointsOfInterest: {
        type: Array as () => PointOfInterest[],
        required: true,
      },
    },
    setup(props) {
      const mapContainer = ref(null);
  
      onMounted(() => {
        const map = L.map(mapContainer.value).fitBounds(getBounds(props.pointsOfInterest));
  
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors',
        }).addTo(map);
  
        props.pointsOfInterest.forEach((poi) => {
          L.marker([poi.latitude, poi.longitude])
            .addTo(map)
            .bindPopup(`<strong>${poi.name}</strong><br>${poi.description}`);
        });
      });
  
      // Helper function to calculate the bounds of all points
      function getBounds(points: PointOfInterest[]) {
        const latLngs = points.map((poi) => L.latLng(poi.latitude, poi.longitude));
        return L.latLngBounds(latLngs);
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
    margin-left: 50%; /* Adjust the margin as needed */
  }
  </style>
  