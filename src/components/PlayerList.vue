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
        outlined
        single-line
        hide-details
        ></v-text-field>

        <v-data-table
          height="inherit"
          :headers="$store.state.player.list.columns"
          :items="$store.state.player.list.content"
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
        >
          <template v-slot:item="{ item }">
            <tr @click="onRowClicked(item)"
            :class="{'blue lighten-3': item.id === $store.state.player.list.selectedId}">
              <td class="text-start"><b>{{ item.full_name }}</b></td>
              <td class="text-start">{{ item.rating }}</td>
              <td class="text-start">{{ item.city }}</td>
            </tr>
          </template>
        </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      playersSearch: null
    }
  },
  methods: {
    onRowClicked(row) {
      this.$store.commit('SET_SELECTED_PLAYER_ID', row.id)
      this.$emit('player-clicked', row.id)
    }
  },
  created() {
    this.$store.dispatch('fetchPlayers')
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
