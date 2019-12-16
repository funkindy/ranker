import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.css'
import '@mdi/font/css/materialdesignicons.css'

import en from 'vuetify/es5/locale/en'
import ru from 'vuetify/es5/locale/ru'

import dateFilter from '@/filters/dateFilter'
import percentFilter from '@/filters/percentFilter'
import roundFilter from '@/filters/roundFilter'

import VueI18n from 'vue-i18n';
import { ENGLISH_TRANSLATIONS } from './translations/en';
import { RUSSIAN_TRANSLATIONS } from './translations/ru';

Vue.config.productionTip = false

Vue.use(Vuetify)
Vue.use(VueI18n)

Vue.filter("date", dateFilter)
Vue.filter("percent", percentFilter)
Vue.filter("round", roundFilter)

const TRANSLATIONS = {
  en: ENGLISH_TRANSLATIONS,
  ru: RUSSIAN_TRANSLATIONS
}

const LOCALE = navigator.language.split('-')[0] || navigator.userLanguage.split('-')[0]

const i18n = new VueI18n({
  locale: LOCALE,
  messages: TRANSLATIONS,
})

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
