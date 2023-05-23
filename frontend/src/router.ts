import {
  createRouter,
  createWebHistory,
  Router,
  RouteRecordRaw,
} from "vue-router";
import Home from "../src/pages/Home.vue";
import Search from "../src/pages/Search.vue";
import Favorites from "./pages/Favorites.vue";
import LogIn from "./pages/LogIn.vue";
import Profile from "./pages/Profile.vue";
import FAQ from "./pages/FAQ.vue";
import Notification from "./components/common/Notification.vue";
import NotificationTest from "./pages/NotificationTest.vue";
export function initRouter(): Router {
  const routes: RouteRecordRaw[] = [
    { path: "/", redirect: "/home" },
    {
      path: "/home",
      component: Home,
    },
    {
      path: "/search",
      component: Search,
    },
    {
      path: "/favorites",
      component: Favorites,
    },
    {
      path: "/login",
      component: LogIn,
    },
    {
      path: "/profile",
      component: Profile,
    },
    {
      path: "/faq",
      component: FAQ,
    },
    {
      path: "/notifications",
      component: NotificationTest
    }
  ];

  return createRouter({
    history: createWebHistory(),
    routes,
  });
}
