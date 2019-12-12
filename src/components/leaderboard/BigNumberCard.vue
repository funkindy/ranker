<template>
  <v-card>
    <v-card-text class="subtitle-1 text-center pb-0">
      {{ total.name }}
    </v-card-text>
    <v-card-text class="display-2 pt-0 font-weight-bold text-center grey--text text--darken-3">
      {{ total.value }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    total: Object
  }
}
</script>