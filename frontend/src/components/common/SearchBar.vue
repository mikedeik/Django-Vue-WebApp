<script setup lang="ts">
import { onMounted, ref } from "vue";
import MultiSelect from "primevue/multiselect";
import InputText from "primevue/inputtext";
import { useRouter } from "vue-router";
import { Category } from "../../Types/Category";
import { getCategories } from "../../API/APICalls.vue";
const router = useRouter();

const categories = ref<Category[]>([]);
const selectedCategories = ref<Category[]>([]);

const location = ref("");

onMounted(() => {

  getCategories().then((res) => {
    if (res.success) {
      res.map((category: any) => {
        categories.value.push({
          value: category.CategoryId,
          name: category.Name
        })
      })
    }
    else {
      alert(res.error);
    }
  }).catch()
})

</script>

<template>
  <div class="root">
        <div class="poi-type">
          <MultiSelect v-model="selectedCategories" display="chip" :options="categories" optionLabel="name"
            placeholder="Κατηγορίες" />
          </div>
        <div class="location">
          <div class="location-input">
            <InputText placeholder="Αναζητήστε εδώ" v-model="location" />
          </div>
        </div>
        <!-- <div class="nomoi-type">
          <MultiSelect v-model="selectedNomoi" display="chip" :options="nomoi" optionLabel="name" placeholder="Νομοί" />
        </div> -->
        <div class="search-icon">
          <div class="pi pi-search" @click="router.push({ path: 'pois' })" />
        </div>
  </div>
</template>

<style scoped lang="scss">

.root {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}
</style>