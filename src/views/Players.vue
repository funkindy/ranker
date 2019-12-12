<template>
  <v-row dense class="mx-0" style="height: 100%">
    <v-navigation-drawer app :clipped="true" width="400">
      <player-list @player-clicked="onPlayerClick"/>
    </v-navigation-drawer>
    <v-col> 
      <player-card
        v-if="playerDetails"
        :playerDetails="playerDetails"
        :playerStats="playerStats"
        :ratingHistory="ratingHistory"
        :matchHistory="matchHistory"
      />
      <v-card v-else>
        <v-card-title primary-title align-center>
          <v-icon left>mdi-arrow-left-circle-outline</v-icon>
          <span>Выберите игрока из списка</span>
        </v-card-title>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios"

import PlayerList from "../components/PlayerList"
import PlayerCard from "../components/PlayerCard"

export default {
  name: "players",
  components: { PlayerCard, PlayerList },
  data() {
    return {
      playerDetails: null,
      playerStats: null,
      ratingHistory: null,
      matchHistory: null
    }
  },
  methods: {
    onPlayerClick(player_id) {
      this.$router.push(`/players/${player_id}`)
    },
    fetchPlayerData(player_id) {
      axios.get(`/api/v1/player/details/${player_id}`).then((response) => {
        this.playerDetails = response.data
      })

      axios.get(`/api/v1/player/stats/${player_id}`).then((response) => {
        this.playerStats = response.data
      })

      axios.get(`/api/v1/history/rating/${player_id}`).then((response) => {
        this.ratingHistory = response.data
      })

      axios.get(`/api/v1/history/match/${player_id}`).then((response) => {
        this.matchHistory = response.data
      })
    },
    resetPlayerData() {
      this.playerDetails = null
      this.playerStats = null
      this.ratingHistory = null
      this.matchHistory = null
    }
  },
  watch: {
    '$route' (to, from) {
      if (to.params.id) {
        this.fetchPlayerData(to.params.id)
      } else {
        this.resetPlayerData()
      }
    }
  },
  created() {
    if (this.$route.params.id) {
      this.fetchPlayerData(this.$route.params.id)
    }
  }
}
</script>
