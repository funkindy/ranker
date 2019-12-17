import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n';

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'
import '@mdi/font/css/materialdesignicons.css'

import en from 'vuetify/es5/locale/en'
import ru from 'vuetify/es5/locale/ru'

import dateFilter from '@/filters/dateFilter'
import percentFilter from '@/filters/percentFilter'
import roundFilter from '@/filters/roundFilter'


Vue.config.productionTip = false

Vue.use(Vuetify)

Vue.filter("date", dateFilter)
Vue.filter("percent", percentFilter)
Vue.filter("round", roundFilter)

const LOCALE = navigator.language.split('-')[0] || navigator.userLanguage.split('-')[0]

new Vue({
  router,
  store,
  i18n,
  vuetify: new Vuetify({
    lang: {
      locales: { en, ru },
      current: LOCALE,
    }
  }),
  render: h => h(App)
}).$mount('#app')
