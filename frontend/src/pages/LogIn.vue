<template>
  <div class= "root">
    <div class="header">
      <Header/>
    </div>
     <div class="login-form">
    <form @submit.prevent="handleLogin"
      @submit="handleLogin">
      <h2>Login</h2>
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="data.username" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="data.password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
  </div>
</template>

<script setup lang="ts">

import { ref } from "vue";
import Header from "../components/common/Header.vue";
import {loginAuthenticate} from "../API/APICalls.vue";
import {useRouter} from "vue-router";
import InputText from 'primevue/inputtext';

const router = useRouter();

const data = ref({
  username: "",
  password: ""
});

const handleLogin = async () => {
  console.log("runs");
  loginAuthenticate(data.value).then(
      (res) => {
        console.log(res);
        localStorage.setItem('accessToken', res.access);
        localStorage.setItem('refreshToken', res.refresh);
        router.push({ path: 'home' });

      }
  ).catch((e) =>{
    console.log(e.error);
  })
}

</script>

<style scoped lang="scss">

.root{
  display: flex;
  flex-direction: column;
  align-items: center;
   width: 100%;
  height: 100%;
}
.header {
  width: 100%;
  height: 10%;
}

.login-form {
  max-width: 300px;
  min-height: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  background-color: #fff;

  form {
    display: flex;
    flex-direction: column;
  }

  h2 {
    margin-bottom: 20px;
    text-align: center;
  }

  .form-group {
    margin-bottom: 20px;

    label {
      display: block;
      font-weight: bold;
    }

    input[type='text'],
    input[type='password'] {
      width: 100%;
      padding: 10px;
      font-size: 16px;
      border-radius: 4px;
      border: 1px solid #ccc;
    }
  }

  button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover {
      background-color: #45a049;
    }
  }
}
</style>
