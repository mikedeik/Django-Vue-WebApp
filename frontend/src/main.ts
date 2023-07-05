import { createApp } from "vue";
import App from "./App.vue";
import "primeicons/primeicons.css";
import "primevue/resources/themes/saga-purple/theme.css";
import "primevue/resources/primevue.min.css";
import PrimeVue from "primevue/config";
import "bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import { initRouter } from "../src/router";

const router = initRouter();
const app = createApp(App);
app.use(router).use(PrimeVue).mount("#app");
