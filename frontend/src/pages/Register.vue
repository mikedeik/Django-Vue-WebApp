<template>
  <div class="container">
    <div class="header">
      <Header></Header>
    </div>
    <div class="content">
      <h1>Register</h1>
      <div class="mb-3">
        <label for="name" class="form-label">Όνομα</label>
        <input
          v-model="first_name"
          type="text"
          class="form-control"
          id="name"
          required
        />
      </div>
      <div class="mb-3">
        <label for="name" class="form-label">Επίθετο</label>
        <input
          v-model="last_name"
          type="text"
          class="form-control"
          id="last_name"
          required
        />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          v-model="email"
          type="email"
          class="form-control"
          id="email"
          required
        />

      <div class="mb-3">
        <label for="surname" class="form-label">Όνομα Χρήστη</label>
        <input
          v-model="username"
          type="text"
          class="form-control"
          id="surname"
          required
        />
      </div>

      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Κωδικός</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          id="password"
          required
        />
        <div class="mb-3">
        <label for="name" class="form-label">Επιβεβαίωση Κωδικού</label>
        <input
          v-model="confirmPassword"
          type="text"
          class="form-control"
          id="confirmPassword"
          required
        />
      </div>
      </div>
      <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
      </div>
      <button type="submit" @click="submitForm" class="btn btn-primary">
        Submit
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "../components/common/Header.vue";
import { register } from "../API/APICalls.vue";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// Define reactive variables using `ref`
const first_name = ref("");
const last_name = ref("");
const username = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const error = ref("");

// Define the submitForm method
const submitForm = async () => {
  const data = {
    username: username.value,
    first_name: first_name.value,
    last_name: last_name.value,
    password: password.value,
    password2: confirmPassword.value,
    email: email.value,
  };
  await register(data).then(() => router.push({ path: "home" }));
};
</script>

<style scoped lang="scss">
.header {
  min-width: 100%;
  height: 10%;
}
.container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.form-control {
  border: 1px solid #000;
  width: 100%;
}
</style>
