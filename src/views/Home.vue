<template>
  <v-row class="ma-0" style="height: 100%">
    <v-col cols="12" md="6">
      <v-row>
        <v-col
          class="pt-0"
          v-for="total in totals"
          :key="total.id"
        >
          <BigNumberCard :total="total" />
        </v-col>
      </v-row>

      <LeadersCard
        :title="$t('leaderboard.top')"
        :leaders="leaders"
      />
      
    </v-col>
  <v-col> 
      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.most_games')"
        :content="maxes.games"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
      />

      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.winrate')"
        :content="maxes.winrate"
        valueFilter="percent"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
      />

      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.effective')"
        :content="maxes.efficiency"
        valueClass="green--text text--accent-4"
      />
    </v-col>
    <v-col>
      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.rise')"
        :content="weekly.best"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
        dense
      />
      <SimpleCard 
        icon="mdi-thumb-down"
        :title="$t('leaderboard.fall')"
        :content="weekly.worst"
        valueClass="red--text text--accent-4"
        dense
      />
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios"
import SimpleCard from '../components/leaderboard/SimpleCard' 
import LeadersCard from '../components/leaderboard/LeadersCard' 
import BigNumberCard from '../components/leaderboard/BigNumberCard' 


export default {
  name: "home",
  components: { SimpleCard, LeadersCard, BigNumberCard },
  data() {
    return {
      leaders: [],
      weekly: {},
      maxes: [],
      totals: []
    }
  },
  created() {

    this.$store.commit('ALTER_LOADING_STATE', true)

    axios.get('/api/v1/players/leaderboard').then((response) => {
      this.weekly = response.data.weekly
      this.leaders = response.data.leaders
      this.maxes = response.data.maxes
      this.totals = response.data.totals

      this.$store.commit('ALTER_LOADING_STATE', false)
    })


  }
};
</script>