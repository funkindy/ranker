import Vue from 'vue'
import Vuex from 'vuex'
import i18n from './i18n';
import axios from "axios"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLoading: false,
    hands: {
      R: i18n.t('player_card.info.hand_right'),
      L: i18n.t('player_card.info.hand_left')
    },
    player: {
      list: {
        selectedId: -1,
        content: [],
        columns: [
          {text: i18n.t("players_list.name_col"), value: "full_name", width: 180},
          {text: i18n.t("players_list.rating_col"), value: 'rating', width: 100},
          {text: i18n.t("players_list.city_col"), value: 'city', width: 80}
        ]
      },
      details: {
        playerInfo: null,
        playerStats: null,
        ratingHistory: null,
        matchHistory: null,
        matchHistoryColumns: [
          // {text: "id", value: "id"},
          {text: i18n.t('player_card.history.cols.event_date'), value: "event_date", width: "10%"},
          {text: i18n.t('player_card.history.cols.event_short_name'), value: "event_short_name", width: "10%"},
          {text: i18n.t('player_card.history.cols.score'), value: "score", width: "4%"},
          {text: i18n.t('player_card.history.cols.rating'), value: "rating", width: "2%"},
          {text: i18n.t('player_card.history.cols.opponent_name'), value: "opponent_name", width: "10%"},
          {text: i18n.t('player_card.history.cols.opponent_rating'), value: "opponent_rating", width: "1%"},
          {text: i18n.t('player_card.history.cols.delta'), value: "delta", width: "1%"}
        ]
      }
    },
    lb: {
      leaders: [],
      weekly: {},
      maxes: [],
      totals: []
    }
  },
  mutations: {
    SET_LB_WEEKLY(state, weekly) {
      state.lb.weekly = weekly
    },
    SET_LB_LEADERS(state, leaders) {
      state.lb.leaders = leaders
    },
    SET_LB_MAXES(state, maxes) {
      state.lb.maxes = maxes
    },
    SET_LB_TOTALS(state, totals) {
      state.lb.totals = totals
    },
    SET_LOADING_STATUS(state, isLoading) {
      state.isLoading = isLoading
    },
    SET_PLAYER_LIST(state, player_list) {
      state.player.list.content = player_list
    },
    SET_SELECTED_ID(state, selectedId) {
      state.player.list.selectedId = selectedId
    },
    SET_PLAYER_INFO(state, playerInfo) {
      state.player.details.playerInfo = playerInfo
    },
    SET_PLAYER_STATS(state, playerStats) {
      state.player.details.playerStats = playerStats
    },
    SET_PLAYER_RATING_HISTORY(state, ratingHistory) {
      state.player.details.ratingHistory = ratingHistory
    },
    SET_PLAYER_MATCH_HISTORY(state, matchHistory) {
      state.player.details.matchHistory = matchHistory
    }
  },
  actions: {
    fetchLeaderboard(context) {
      context.commit('SET_LOADING_STATUS', true)
      axios.get('/api/v1/players/leaderboard').then((response) => {
        context.commit('SET_LB_WEEKLY', response.data.weekly)
        context.commit('SET_LB_LEADERS', response.data.leaders)
        context.commit('SET_LB_MAXES', response.data.maxes)
        context.commit('SET_LB_TOTALS', response.data.totals)
        context.commit('SET_LOADING_STATUS', false)
      })
    },
    fetchPlayers(context) {
      context.commit('SET_LOADING_STATUS', true)
      axios.get('/api/v1/players/all').then((response) => {
        context.commit('SET_PLAYER_LIST', response.data)
        context.commit('SET_LOADING_STATUS', false)
      })
    },
    fetchPlayerDetails(context, player_id) {
      
      context.commit('SET_LOADING_STATUS', true)
      
      axios.get(`/api/v1/player/details/${player_id}`).then((response) => {
        context.commit('SET_PLAYER_INFO', response.data)
      })

      axios.get(`/api/v1/player/stats/${player_id}`).then((response) => {
        context.commit('SET_PLAYER_STATS', response.data)
      })

      axios.get(`/api/v1/history/rating/${player_id}`).then((response) => {
        context.commit('SET_PLAYER_RATING_HISTORY', response.data)
      })

      axios.get(`/api/v1/history/match/${player_id}`).then((response) => {
        context.commit('SET_PLAYER_MATCH_HISTORY', response.data)
        context.commit('SET_LOADING_STATUS', false)
      })
    },
    resetPlayerDetails(context) {
      context.commit('SET_PLAYER_INFO', null)
      context.commit('SET_PLAYER_STATS', null)
      context.commit('SET_PLAYER_RATING_HISTORY', null)
      context.commit('SET_PLAYER_MATCH_HISTORY', null)
    }
  }
})
