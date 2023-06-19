<template>
  <div class="home-container">
    <div class="header">
      <Header></Header>
    </div>
    <div class="content">
      <div class="search-bar">
        <div class="location">
          <div class="location-title">Location</div>
          <div class="location-input">
            <InputText placeholder="Where are you going?" v-model="location" />
          </div>
        </div>
        <div class="poi-type">
          <MultiSelect v-model="selectedPois" display="chip" :options="poiOptions" optionLabel="name" placeholder="Τύπος POI"  />
        </div>
        <div class="activity-type">
          <MultiSelect v-model="selectedActivities" display="chip" :options="activityOptions" optionLabel="name" placeholder="Δραστηριότητα" />
        </div>
        <div class="more-filters">
          More Filters
        </div>
        <div class="search-icon">
          <div class="pi pi-search" @click="router.push({path: 'pois'})"/>
        </div>
      </div>
      <div class="main-content">
        <div class="main-content-title">Not sure where to go? Perfect</div>
        <div class="main-content-button">I'm flexible</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Header from "../components/common/Header.vue";
import InputText from 'primevue/inputtext';
import MultiSelect from 'primevue/multiselect';
import { stringifyExpression } from "@vue/compiler-core";
import {useRouter} from "vue-router";

const router = useRouter();

const poiOptions=ref([{
  name:'Λίμνες',
  value:'Limnes'
},{
  name:'Παρκα',
  value:'Parka'
},])

const selectedPois=ref<Array<{name:string ,value:string}>>([])

const activityOptions=ref([{
  name:'Πεζοπορία',
  value:'Pezoporia'
},{
  name:'Κύνηγι',
  value:'Kinigi'
},])

const selectedActivities=ref<Array<{name:string ,value:string}>>([])

const location=ref("")
</script>

<style scoped lang="scss">
.home-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction:column;
}

.header {
  min-width: 100%;
  height: 10%;
}
.content {
  height: 90%;
  width: 100%;
  //overflow: auto;
}
.search-bar {
  height: 10%;
  width:100%;
  display: flex;
  align-items: center;
  justify-content: space-evenly;

}

.main-content {
  height: 90%;
   //background-image: url(../assets/forest.jpg);
   //background-size: cover;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  &-title {
    color: white;
    font-size: 60px;
    font-weight: 500;
    margin-bottom: 2%;
  }
  &-button {
    width: 132px;
    height: 56px;
    background-color: white;
    color: #eb9317;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 100px;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 10%;
  }

  &::before {
    content: "";
    background-image: url(../assets/forest.jpg);
    background-size: cover;
    border-radius: 12px;
    position: absolute;
    top: 19%;
    right: 0px;
    bottom: 0px;
    left: 0px;
    filter: brightness(0.8);
    z-index: -1;
  }
}

.p-inputtext{

  &:focus-visible {
    outline: none !important;
  }
}
</style>
