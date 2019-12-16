import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLoading: false
  },
  mutations: {
    ALTER_LOADING_STATE (state, isLoading) {
      state.isLoading = isLoading
    }
  }
})