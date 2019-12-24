<template>
  <v-card>
    <v-subheader>
      <v-icon left>mdi-trophy</v-icon>
      {{ title }}
    </v-subheader>
    <v-list flat dense>
      <v-list-item-group>
        <v-row dense
          align="center" justify="center"
          v-for="(leader, index) in leaders"
          :key="leader.id"
          @click="playerClick(leader.id)"
        >
          <v-col cols="12" md="9">
            <v-list-item>
              <v-list-item-avatar>
                #{{ index + 1 }}
              </v-list-item-avatar>
              <v-list-item-avatar  color="grey" class="ml-2 mr-0">
              </v-list-item-avatar>
              <v-list-item-content class="ml-2 text-center">
                <v-list-item-title>
                   <v-icon
                    dense
                    v-if="index + 1 <= 3"
                    :class="$store.state.placeClasses[index + 1]"
                  >
                      mdi-star-circle
                  </v-icon>
                  {{ leader.name }}
                </v-list-item-title>
                <v-list-item-subtitle>{{ leader.city }}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-content class="subtitle-1 text-center">
                <v-list-item-title :title="$t('player_card.rating')">
                  {{ leader.rating | round(2) }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-col>
          <v-col cols="8" md="3" class="pr-4">
            <v-sheet
            :title="$t('player_card.chart.name')"
            elevation="0">
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
          </v-col>
        </v-row>
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
      gradient: ['#f72047', '#ffd200', '#1feaea']
    }
  },
  methods: {
    playerClick(player_id) {
      let url = `/players/${player_id}`
      window.open(url, '_blank')
    }
  }
}
</script>
