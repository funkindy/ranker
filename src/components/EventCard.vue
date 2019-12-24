<template>
  <v-card>
    <v-card-title>
      <div class="overline">{{ $t("event_card.title") }}</div>
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col>      
          <BigNumberCard :total="totalEvents"/>
        </v-col>
        <v-col>      
          <BigNumberCard :total="avgRating"/>
        </v-col>
        <v-col>
          <BigNumberCard :total="avgPlayers"/>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card>
            <v-card-title>
              <div class="overline">{{ $t("event_card.recent_events") }}</div>
            </v-card-title>
            <v-card-text>
              <v-card
                v-for="event in info.recent"
                class="mb-1"
                :key="event.id"
              >
                <v-card-title>
                  {{ event.event_date | date }}
                </v-card-title>

                <v-card-text class="text--primary">
                  <div>{{ $t("event_card.players_count") }}: <b>{{ event.players_count }}</b></div>
                  <div>{{ $t("event_card.avg_rating") }}: <b>{{ event.avg_rating | round(2)}}</b></div>
                  
                  <v-list dense>
                    <v-list-item
                      v-for="player in event.places"
                      :key="player.id"
                      @click="playerClick(player.id)"
                    >
                      <v-list-item-icon>
                        <v-icon :class="$store.state.placeClasses[player.place]">
                          mdi-circle-slice-8
                        </v-icon>
                      </v-list-item-icon>
                      {{ player.name }}
                      ({{ player.rating | round(2) }})
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-card-text>
          </v-card>
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
  methods: {
    playerClick(player_id) {
      let url = `/players/${player_id}`
      window.open(url, '_blank')
    },
  },
  computed: {
    totalEvents() {
      return {
        name: this.$t("event_card.total_events"),
        value: this.info.total_events
      }
    },
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