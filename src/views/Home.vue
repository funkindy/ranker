<template>
  <v-row class="ma-0" style="height: 100%">
    <v-col cols="12" md="6">
      <v-row>
        <v-col
          class="pt-0"
          v-for="total in $store.state.lb.totals"
          :key="total.id"
        >
          <BigNumberCard :total="total" />
        </v-col>
      </v-row>

      <LeadersCard
        class="mt-2"
        :title="$t('leaderboard.top')"
        :leaders="$store.state.lb.leaders"
      />
    </v-col>
    <v-col>
      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.most_games')"
        :content="$store.state.lb.maxes.games"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
      />

      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.winrate')"
        :content="$store.state.lb.maxes.winrate"
        valueFilter="percent"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
      />

      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.effective')"
        :content="$store.state.lb.maxes.efficiency"
        valueClass="green--text text--accent-4"
      />
    </v-col>
    <v-col>
      <SimpleCard
        icon="mdi-thumb-up"
        :title="$t('leaderboard.rise')"
        :content="$store.state.lb.weekly.best"
        valueClass="green--text text--accent-4"
        cardClass="mb-3"
        dense
      />
      <SimpleCard
        icon="mdi-thumb-down"
        :title="$t('leaderboard.fall')"
        :content="$store.state.lb.weekly.worst"
        valueClass="red--text text--accent-4"
        dense
      />
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";
import SimpleCard from "../components/leaderboard/SimpleCard";
import LeadersCard from "../components/leaderboard/LeadersCard";
import BigNumberCard from "../components/leaderboard/BigNumberCard";

export default {
  name: "home",
  components: { SimpleCard, LeadersCard, BigNumberCard },
  created() {
    this.$store.dispatch("fetchLeaderboard");
  },
};
</script>
