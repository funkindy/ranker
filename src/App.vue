<template>
  <div id="app">
    <component :is="layout">
      <router-view />
    </component>
  </div>
</template>

<script>
import MainLayout from "@/layouts/MainLayout";
import EmptyLayout from "@/layouts/EmptyLayout";


export default {
  name: "app",
  components: { MainLayout, EmptyLayout },
  computed: {
    layout() {
      return this.$route.meta.layout;
    }
  }
};
</script>

<style>
/* Padding is not needed as we use progress-bar in toolbar extension */
.v-toolbar__extension {
  padding: 0px !important;
}
</style>