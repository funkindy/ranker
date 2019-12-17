<template>
  <v-card style="height: 100%">
    <v-card-title>
      <div class="overline">{{ $t("player_card.name") }}</div>
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="4" md="2" class="text-center" justify="center">
          <v-avatar size="60">
            <img
              src="https://eitrawmaterials.eu/wp-content/uploads/2016/09/empty-avatar.jpg"
            >
          </v-avatar>
          <br>
          <div :title="`${$t('player_card.rating')} ${playerInfo.rating}`">
            <v-icon class="red--text text--lighten-1">mdi-star-circle-outline</v-icon>
            <span
            style="vertical-align:middle"
            class="font-weight-bold blue--text subtitle-2">
              {{ playerInfo.rating }}
            </span>
          </div>
        </v-col>
        <v-col class="body-2 font-weight-light">
          <p class="headline mb-1">{{ fullname }}</p>
          <span class="font-weight-bold">{{ $t("player_card.city") }}:</span> {{ playerInfo.city }}<br>
          <v-spacer></v-spacer>
          <span class="font-weight-bold">{{ $t("player_card.date_of_birth") }}:</span>  {{ playerInfo.date_of_birth | date }}
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <v-row>
        <v-col style="overflow: auto">
          <v-tabs 
            color="blue lighten-1"
            :vertical="false"
            grow
          >
            <v-tab :title="$t('player_card.info.name')"><v-icon>mdi-chart-bubble</v-icon></v-tab>
            <v-tab :title="$t('player_card.chart.name')"><v-icon>mdi-chart-areaspline</v-icon></v-tab>
            <v-tab :title="$t('player_card.history.name')"><v-icon>mdi-file-chart-outline</v-icon></v-tab>

           <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.info.name') }}</p>
              <v-list disabled v-if="playerStats">
                <v-list-item-group>
                  <v-list-item
                    v-for="(item, index) in statItems"
                    :key="index"
                  >
                    <v-list-item-icon>
                      <v-icon v-text="item.icon"></v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title v-html="item.title"></v-list-item-title>
                      <v-list-item-subtitle v-html="item.subtitle"></v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-tab-item>

            <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.chart.name') }}</p>
              <line-chart
              :height="155"
              :chartData="chartData"
              :options="chartOptions" />
            </v-tab-item>

            <v-tab-item class="pa-2">
              <p class="overline">{{ $t('player_card.history.name') }}</p>
              <v-data-table
                :headers="$store.state.player.details.matchHistoryColumns"
                :items="matchHistory"
                :dense="true"
                :items-per-page="10"
                :hide-default-footer="true"
                class="elevation-0"
              >
                <template v-slot:item.event_date="{ item }">
                  {{ item.event_date | date}}
                </template>
                <template v-slot:item.score="{ item }">
                  <b>{{ item.score }}</b>
                </template>
                <template v-slot:item.delta="{ item }">
                  <span :class="getDeltaClass(item)">{{ getDeltaValue(item) }}</span>
                </template>
              </v-data-table>
            </v-tab-item>
          </v-tabs>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import LineChart from "@/components/LineChart"


export default {
  components: { LineChart },
  props: {
    playerInfo: Object,
    playerStats: Object,
    ratingHistory: Array,
    matchHistory: Array
  },
  data() {
    return {
      chartOptions: {
        legend: {
          display: false
        }
      }
    }
  },
  methods: {
    getDeltaClass(item) {
      if (item.result) {
        return 'green--text text--accent-4 font-weight-bold'
      } else {
        return 'red--text text--accent-4 font-weight-bold'
      }
    },
    getDeltaValue(item) {
      if (item.result) {
        return item.delta
      } else {
        return item.delta * -1
      }
    }
  },
  computed: {
    fullname () {
      return `${this.playerInfo.first_name} ${this.playerInfo.last_name}`
    },
    statItems () {
      return [
        { 
          icon: "mdi-chart-donut",
          title: `${this.$t('player_card.info.total_games')}: <b>${this.playerStats.total_games}</b>`,
          subtitle: `( <span class="green--text text--accent-4 font-weight-bold">${this.playerStats.win_count}</span> /
                      <span class="red--text text--accent-4 font-weight-bold">${this.playerStats.lose_count }</span> )
                      ${this.$options.filters.percent(this.playerStats.win_count / this.playerStats.total_games, 2)}`
        },
        {
          icon: "mdi-summit",
          title: `${this.$t('player_card.info.best_rating')}: <b>${this.$options.filters.round(
            this.playerStats.best_rating.rating, 2
          )}</b>`,
          subtitle: this.$options.filters.date(this.playerStats.best_rating.date)
        },
        {
          icon: "mdi-account-outline",
          title: this.$t('player_card.info.username'),
          subtitle: this.playerInfo.username
        },
        {
          icon: "mdi-hand",
          title: this.$t('player_card.info.hand'),
          subtitle: this.$store.state.hands[this.playerInfo.hand]
        },
        {
          icon: "mdi-rocket",
          title: this.$t('player_card.info.equipment'),
          subtitle: this.playerInfo.equipment
        }
      ]

    },
    chartData () {
      var label = this.fullname
      var xlabels = []
      var dataPoints = []

      if (this.ratingHistory) {
        this.ratingHistory.forEach((record, index) => {
          dataPoints.push({ x: index, y: record.rating})
          xlabels.push(record.date)
        })
      }

      return {
        labels: xlabels,
        datasets: [{
          borderColor: 'rgba(50, 115, 220, 0.5)',
          backgroundColor: 'rgba(50, 115, 220, 0.1)',
          label: label,
          data: dataPoints
        }]
      }
    }
  }
};
</script>

<style>
  .v-data-table table tr td {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
