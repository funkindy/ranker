<template>
  <v-app-bar :elevation="2" dense app :clipped-left="true">
    <img
      style="max-width: 32px; max-height: 32px"
      class="mr-3"
      src="/static/logo.png"
    />
    <v-toolbar-title>RANKER</v-toolbar-title>

    <v-spacer></v-spacer>

    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn text v-for="item in menu"
        :key="item.icon"
        :to="item.to"
        :href="item.href"
        :target="item.target"
      >
        <v-icon :left="true">{{ item.icon }}</v-icon>
        {{ item.name }}
      </v-btn>
    </v-toolbar-items>
    <v-menu class="hidden-md-and-up">
      <template v-slot:activator="{ on }">
        <v-btn text v-on="on">
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item v-for="item in menu" :key="item.icon">
          <v-btn text 
            :to="item.to"
            :href="item.href"
            :target="item.target"
          >
            <v-icon :left="true">{{ item.icon }}</v-icon>
            {{ item.name }}
          </v-btn>
        </v-list-item>   
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
export default {
  data() {
    return {
      menu: [
        {name: this.$t("nav.main"), icon: "mdi-home-outline", to: "/"},
        {name: this.$t("nav.players"), icon: "mdi-account", to: "/players"},
        {
          name: this.$t("nav.link"),
          icon: "mdi-link",
          href: "https://tv.ittf.com/",
          target: "_blank"}
      ]
    }
  }
};
</script>

<style scoped>
  a {
    text-decoration: none;
  }
</style>