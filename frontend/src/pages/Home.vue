<template>
  <div class="home-container">
    <div class="header">
      <Header></Header>
    </div>

    <div class="content">
      <div class="main-content">
        <div class="main-content-title">Not sure where to go? Perfect</div>
        <Button class="main-content-button" @click="router.push({path: 'pois'})">Αναζήτηση Περιοχών</Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import Header from "../components/common/Header.vue";
import InputText from "primevue/inputtext";
import MultiSelect from "primevue/multiselect";
import { useRouter } from "vue-router";
import { Category } from "../Types/Category";
import { getCategories } from "../API/APICalls.vue";
import SearchBar from "../components/common/SearchBar.vue";
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

<style scoped lang="scss">
.home-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
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
  width: 100%;
  //display: flex;
  //align-items: center;
  //justify-content: space-evenly;
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
    margin-bottom: 20%;
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

.p-inputtext {
  &:focus-visible {
    outline: none !important;
  }
}
</style>
