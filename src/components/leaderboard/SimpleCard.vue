<template>
  <v-card :class="cardClass">
    <v-subheader>
      <v-icon left>{{ icon }}</v-icon>
      {{ title }}
    </v-subheader>
    <v-list flat :dense="dense">
      <v-list-item-group>
        <v-list-item
          v-for="item in content"
          :key="item.id"
          @click="playerClick(item.id)"
          >
          <v-list-item-content>
            <v-list-item-title>{{ item.name }}</v-list-item-title>
          </v-list-item-content>
          <v-list-item-icon>
            <span class="font-weight-bold ml-3"
              :class="valueClass"
              >
              {{ filter(item.value) }}
            </span>
          </v-list-item-icon>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>

export default {
  props: {
    dense: Boolean,
    icon: String,
    title: String,
    content: Array,
    valueFilter: String,
    cardClass: String,
    valueClass: String
  },
  methods: {
    playerClick(player_id) {
      let url = `/players/${player_id}`
      window.open(url, '_blank')
      // To open same window:
      // this.$router.push(url)
    }
  },
  computed: {
    filter() {
      if (this.valueFilter == "percent") {
        return this.$options.filters.percent
      } else {
        return this.$options.filters.round
      }
    }
  }
}

</script>
