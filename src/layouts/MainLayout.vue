<template>
  <v-app id="app">
    <navbar />
    <v-content>
      <v-container fill-height fluid>
          <router-view />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import Navbar from "@/components/Navbar";

export default {
  name: "main-layout",
  components: { Navbar },
  data() {
    return {

    }
  }
};
</script>
