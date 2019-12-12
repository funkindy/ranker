<template>
  <v-card>
    <v-subheader>
      <v-icon left>mdi-trophy</v-icon>
      {{ title }}
    </v-subheader>
    <v-list flat dense>
      <v-list-item-group>
        <v-list-item
          v-for="(leader, index) in leaders"
          :key="leader.id"
          @click="playerClick(leader.id)"
        >
          <v-list-item-avatar>
            #{{ index + 1 }}
          </v-list-item-avatar>
          <v-list-item-avatar color="grey">
          </v-list-item-avatar>
          <v-list-item-content class="ml-3">
            <v-list-item-title>{{ leader.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ leader.city }}</v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-content>
            <v-list-item-title class="subtitle-1">
              <v-chip
                class="ma-2"
                title="Рейтинг"
                :color="getPlaceBgColor(index + 1)"
                :text-color="getPlaceColor(index + 1)"
              >
                <v-icon v-if="index + 1 <= 3" dense>
                  mdi-star
                </v-icon>
                  {{ leader.rating | round(2) }}
              </v-chip>
            </v-list-item-title>
          </v-list-item-content>
          <v-sheet
          title="Тренд рейтинга"
          elevation="1"
          width="160px">
            <v-sparkline
              :value="leader.rating_trend"
              :smooth="25"
              :padding="8"
              :gradient="gradient"
              :line-width="4"
              :auto-line-width="true"
              :auto-draw-duration="1000"
              :auto-draw="true"
              :fill="false"
            ></v-sparkline>
          </v-sheet>
        </v-list-item>
      </v-list-item-group>
    </v-list>
  </v-card>
</template>

<script>
export default {
  props: {
    title: String,
    leaders: Array
  },
  data() {
    return {
      // gradient: ['#f72047', '#ffd200', '#1feaea'],
      gradient: ['#00C853', '#ffd200', '#D50000'],
      placeColor: {
        1: "#fee001",
        2: "#A7A7AD",
        3: "#824A02"
      }
    }
  },
  methods: {
      playerClick(player_id) {
        let url = `/players/${player_id}`
        window.open(url, '_blank')
        // To open same window:
        // this.$router.push(url)
      },
      getPlaceBgColor(place) {
        let color = "white"
        let alpha = 35
        if (place <= 3) {
          color = `${this.placeColor[place]}${alpha}`
        } 
        return color
      },
      getPlaceColor(place) {
        let color = "black"
        if (place <= 3) {
          color = this.placeColor[place]
        } 
        return color
      }
  }
}
</script>