<template>
  <div class="poi-card">
    <img :src="poi.image" :alt="poi.name" class="poi-image" />
    <div class="poi-details">
      <h3 class="poi-title">{{ poi.name }}</h3>
      <p class="poi-description">{{ poi.description }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { PointOfInterest } from '../../Types/PointOfInterest';

export default defineComponent({
  props: {
    poi: {
      type: Object as () => PointOfInterest,
      required: true,
    },
  },
});
</script>

<style scoped>
.poi-card {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
}

.poi-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
  margin-right: 16px;
}

.poi-details {
  flex: 1;
}

.poi-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.poi-description {
  margin: 8px 0;
}
</style>
