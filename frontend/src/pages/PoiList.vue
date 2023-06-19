<template>
<div>
  <h2>PoiList</h2>
  <div>
      <div v-for="poi in pois">
        {{ poi.Name }} - {{poi.CategoryID}}
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

interface Poi {
  name: string;
  // Add other properties here if necessary
}
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

// watch(pois, () =>{
//   pois.value.map((p: any) => {
//     new_pois.value.push({
//       name: p.Name
//     })
//   });
//
//   console.log(new_pois.value);
// })

</script>

<style scoped lang="scss">

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