import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios"
import i18n from './i18n'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLoading: false,
    hands: {
      R: i18n.t('player_card.info.hand_right'),
      L: i18n.t('player_card.info.hand_left')
    },
    placeClasses: {
      1: "yellow--text text--accent-4",
      2: "blue-grey--text text--lighten-4",
      3: "brown--text text--darken-1"
    },
    lb: {
      leaders: [],
      weekly: {},
      maxes: [],
      totals: []
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
        notFound: false,
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
    event: {
      list: {
        selectedId: -1,
        content: []
      },
      details: {
        info: {}
      }
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
    SET_PLAYER_LIST(state, playerList) {
      state.player.list.content = playerList
    },
    SET_SELECTED_PLAYER_ID(state, selectedId) {
      state.player.list.selectedId = selectedId
    },
    SET_PLAYER_NOT_FOUND(state) {
      state.player.details.notFound = true
    },
    SET_PLAYER_FOUND(state) {
      state.player.details.notFound = false
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
    },
    SET_EVENTS_LIST(state, eventsList) {
      state.event.list.content = eventsList
    },
    SET_SELECTED_EVENT_ID(state, event_id) {
      state.event.list.selectedId = event_id
    },
    SET_EVENT_DETAILS(state, eventInfo) {
      state.event.details.info = eventInfo
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

      if (typeof player_id === "undefined") {
        // if we at players page just reset the find status
        context.commit('SET_PLAYER_FOUND')
        return
      }

      if (isNaN(player_id)) {
        // If not a nuber somehow provided
        context.dispatch('resetPlayerDetails')
        context.commit('SET_PLAYER_NOT_FOUND')
        return
      }

      context.commit('SET_LOADING_STATUS', true)
      
      axios.get(`/api/v1/player/details/${player_id}`).then((response) => {

        context.commit('SET_PLAYER_FOUND')
        context.commit('SET_PLAYER_INFO', response.data)

        // fetch other data if player is found
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

      }).catch(() => {
        // If Django tells there is no such player
        context.dispatch('resetPlayerDetails')
        context.commit('SET_PLAYER_NOT_FOUND')
        context.commit('SET_LOADING_STATUS', false)
      })
    },
    resetPlayerDetails(context) {
      context.commit('SET_PLAYER_FOUND')
      context.commit('SET_PLAYER_INFO', null)
      context.commit('SET_PLAYER_STATS', null)
      context.commit('SET_PLAYER_RATING_HISTORY', null)
      context.commit('SET_PLAYER_MATCH_HISTORY', null)
    },
    fetchEvents(context) {
      context.commit('SET_LOADING_STATUS', true)
      axios.get('/api/v1/events/all').then((response) => {
        context.commit('SET_EVENTS_LIST', response.data)
        context.commit('SET_LOADING_STATUS', false)
      })
    },
    fetchEventDetails(context, event_id) {
      context.commit('SET_LOADING_STATUS', true)
      axios.get(`/api/v1/event/details/${event_id}`).then((response) => {
        context.commit('SET_EVENT_DETAILS', response.data)
        context.commit('SET_LOADING_STATUS', false)
      })
    }
  }
})
