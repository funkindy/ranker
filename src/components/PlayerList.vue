<template>
  <v-card tile> 
    <v-card-title>
        <div class="overline">{{ $t("players_list.name") }}</div>
    </v-card-title>

    <v-card-text>
        <v-text-field
        v-model="playersSearch"
        append-icon="mdi-account-search-outline"
        :label="$t('players_list.search')"
        dense
        single-line
        hide-details
        ></v-text-field>

        <v-data-table
        height="inherit"
        :headers="playersColumns"
        :items="players"
        item-key="id"
        :dense="true"
        :items-per-page="20"
        :fixed-header="false"
        :must-sort="true"
        sortBy="rating"
        :sort-desc="true"
        :search="playersSearch"
        :footer-props="{
            itemsPerPageOptions: [20],
            showFirstLastPage: false
        }"
        @click:row="onRowClicked"
        >
        <template v-slot:item.fullname="{ item }">
            <b>{{ item.last_name }} {{ item.first_name }}</b>
        </template>
        </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios"

export default {
  data() {
    return {
      players: [],
      playersColumns: [
        {text: this.$t("players_list.name_col"), value: "full_name", width: 180},
        {text: this.$t("players_list.rating_col"), value: 'rating', width: 100},
        {text: this.$t("players_list.city_col"), value: 'city', width: 80}
      ],
      playersSearch: null
    }
  },
  methods: {
    onRowClicked(event) {
      this.$emit('player-clicked', event.id)
    }
  },
  created() {
    axios.get('/api/v1/players/all').then((response) => {
      this.players = response.data
    })
  }
}
</script>

<style scope>
  .v-data-table td {
    cursor: pointer;
  }

  .v-data-table th .v-data-table-header__icon {
    font-size: 12px !important
  }
</style>