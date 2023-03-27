<script setup lang="ts"></script>

<template>
  <router-view></router-view>
</template>

<style lang="scss">
@import url("https://fonts.googleapis.com/css?family=Inter:200,300,400,500,600,700,800&display=swap&text=0123456789");
#app {
  height: 100%;
  width: 100%;
}
html,
body {
  font-size: 14px;
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: auto;
}

* {
  font-family: "Inter", "Sofia Pro", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  box-sizing: border-box;
  font-variant-numeric: lining-nums;
  user-select: none;
}

a {
  text-decoration: none;
}
button {
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  margin: 0;
  user-select: none;
  -webkit-user-select: none;
  &:disabled {
    cursor: default;
    opacity: 50%;
  }
  &:active {
    opacity: 50%;
  }
}

.p-link {
  box-shadow: none !important;
}

.p-dropdown {
  box-shadow: none !important;
}

input,
textarea {
  &:focus-visible {
    outline: none !important;
  }
}
textarea {
  resize: none;
}
</style>
