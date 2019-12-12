<template>
  <div id="app">
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script>
import MainLayout from "@/layouts/MainLayout";

export default {
  name: "app",
  components: { MainLayout },
  computed: {
    layout() {
      return this.$route.meta.layout;
    }
  }
};
</script>
