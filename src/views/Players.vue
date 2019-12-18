<template>
  <v-row dense class="mx-0" style="height: 100%">
    <v-navigation-drawer app :clipped="true" width="400" v-model="showSider">
      <player-list @player-clicked="onPlayerClick"/>
    </v-navigation-drawer>
    <v-col> 
      <player-card
        v-if="$store.state.player.details.playerInfo"
        :playerInfo="$store.state.player.details.playerInfo"
        :playerStats="$store.state.player.details.playerStats"
        :ratingHistory="$store.state.player.details.ratingHistory"
        :matchHistory="$store.state.player.details.matchHistory"

      />
      <v-card v-else>
        <v-card-title primary-title align-center>
          <v-icon left>
            mdi-arrow-left-circle-outline
          </v-icon>
          <span>{{ $t("player_card.placeholder") }}</span>
        </v-card-title>
        <v-card-text
          align-center
          v-if="$store.state.player.details.notFound"
        >
          <v-icon left class="red--text text--accent-2">
            mdi-alert-circle-outline
          </v-icon>
          <span class="red--text text--accent-2">
            {{ $t("player_card.notFound") }}
          </span>
        </v-card-text>
      </v-card>
    </v-col>
      <v-btn
        fab
        small
        fixed
        right
        bottom
        dark
        color="red"
        @click.stop="showSider = !showSider"
      > 
        <v-icon v-if="showSider">mdi-arrow-left</v-icon>
        <v-icon v-else>mdi-account-circle</v-icon>
      </v-btn>
  </v-row>
</template>

<script>
import PlayerList from "../components/PlayerList"
import PlayerCard from "../components/PlayerCard"

export default {
  name: "players",
  components: { PlayerCard, PlayerList },
  data() {
    return {
      showSider: true
    }
  },
  methods: {
    onPlayerClick(player_id) {
      this.$router.push(`/players/${player_id}`).catch(err => {})
    }
  },
  watch: {
    '$route' (to, from) {
      this.$store.dispatch('fetchPlayerDetails', to.params.id)
    }
  },
  created() {
    this.$store.dispatch('fetchPlayerDetails', this.$route.params.id)
  }
}
</script>
