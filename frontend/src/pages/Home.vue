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
            <input placeholder="Where are you going?" />
          </div>
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
import Header from "../components/common/Header.vue";
</script>

<style scoped lang="scss">
.home-container {
  width: 100%;
  height: 100%;
}

.header {
  width: 100%;
  height: 10%;
}
.content {
  height: 90%;
  width: 100%;
  overflow: auto;
}
.search-bar {
  height: 10%;
}
.main-content {
  height: 90%;
  // background-image: url(../assets/forest.jpg);
  // background-size: cover;
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
</style>
