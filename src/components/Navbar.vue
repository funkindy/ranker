<template>
  <v-app-bar :elevation="2" dense app :clipped-left="true">
    <img
      style="max-width: 32px; max-height: 32px"
      class="mr-3"
      src="/static/logo.png"
    />
    <v-toolbar-title>RANKER</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items>
      <v-btn text to="/">
        <v-icon :left="true">mdi-home-outline</v-icon>
        {{ $t("nav.main") }}
      </v-btn>
      <v-btn text to="/players">
        <v-icon :left="true">mdi-account</v-icon>
        {{ $t("nav.players") }}
      </v-btn>
      <!-- Put your own link and link locale -->
      <v-btn text href="https://tv.ittf.com/" target="_blank">
        <v-icon :left="true">mdi-link</v-icon>
        {{ $t("nav.link") }}
      </v-btn>
    </v-toolbar-items>
  </v-app-bar>
</template>

<script>
export default { };
</script>

<style scoped>
  a {
    text-decoration: none;
  }
</style>