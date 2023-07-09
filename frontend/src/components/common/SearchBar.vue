<script setup lang="ts">
import {onMounted, ref, getCurrentInstance, watch} from "vue";
import MultiSelect from "primevue/multiselect";
import InputText from "primevue/inputtext";
import { useRouter } from "vue-router";
import { Category } from "../../Types/Category";
import { getCategories, SearchPois } from "../../API/APICalls.vue";
const router = useRouter();


// Type for searching
type searchType = {
  start: number,
  page: number,
  count: number,
  text : string | null,
  filters: {
    categories : number[] | null,
    keywords : string[] | null,
    // distance: {
    //
    // } | null
  }
};


const props = defineProps(['rows', 'page']);
const categories = ref<Category[]>([]);
const selectedCategories = ref<Category[]>([]);
const instance = getCurrentInstance();
const location = ref("");
const rows = ref<number>(props.rows);
const page = ref<number>(props.page);

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
});

watch(() => props.page,
    async (newPage) => {
      page.value = newPage;
      await searchPOIs();
});



// function to set up the search
const fixSearchData = async () => {
  let data : searchType = {
    start : rows.value,
    page : page.value,
    count : page.value,
    text: null,
    filters: {
      categories: null,
      keywords: null,
      // distance: null
    }
  }
  if(location.value){
    data.text = location.value;
    data.filters.keywords = location.value.split(' ');
  }
  if(selectedCategories){
    data.filters.categories = selectedCategories.value.map((c) => {return c.value});
  }
  if(data.filters.categories?.length === 0){
    data.filters.categories = null;
  }
  return data
}

async function searchPOIs() {
  try {

    let searchData = await fixSearchData();
    console.log(searchData);
    // Make the API call and retrieve the data
    const response = await SearchPois(searchData);

    // Emit the data to the parent component

    if(response.success){
      instance?.emit("search-complete", response.data);
    }

  } catch (error) {
    alert("An error occurred while searching POIs.");
  }

  // await router.push({path: 'pois'});
}

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
          <div class="pi pi-search" @click="searchPOIs" />
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