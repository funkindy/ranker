<template>
  <v-card>
    <v-card-title>
      {{ $t("event_card.title") }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col>      
          <BigNumberCard :total="avgRating"/>
        </v-col>
        <v-col>
          <BigNumberCard :total="avgPlayers"/>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
import BigNumberCard from '@/components/leaderboard/BigNumberCard'

export default {
  components: { BigNumberCard },
  props: {
    info: Object
  },
  computed: {
    avgRating() {
      return {
        name: this.$t("event_card.avg_rating"),
        value: this.$options.filters.round(
          this.info.avg_rating, 2
        )            
      }
    },
    avgPlayers() {
      return {
        name: this.$t("event_card.avg_players"),
        value: this.$options.filters.round(
          this.info.avg_players, 1
        )
      }
    }
  }
}
</script>