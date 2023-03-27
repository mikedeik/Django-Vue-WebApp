import {
  createRouter,
  createWebHistory,
  Router,
  RouteRecordRaw,
} from "vue-router";
import Home from "../src/pages/Home.vue";
export function initRouter(): Router {
  const routes: RouteRecordRaw[] = [
    { path: "/", redirect: "/home" },
    {
      path: "/home",
      component: Home,
    },
  ];

  return createRouter({
    history: createWebHistory(),
    routes,
  });
}
