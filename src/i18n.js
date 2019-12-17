import Vue from 'vue'
import VueI18n from 'vue-i18n'

import { ENGLISH_TRANSLATIONS } from './translations/en'
import { RUSSIAN_TRANSLATIONS } from './translations/ru'

Vue.use(VueI18n)

const TRANSLATIONS = {
  en: ENGLISH_TRANSLATIONS,
  ru: RUSSIAN_TRANSLATIONS
}

const LOCALE = navigator.language.split('-')[0] || navigator.userLanguage.split('-')[0]

const i18n = new VueI18n({
  locale: LOCALE,
  messages: TRANSLATIONS,
})

export default i18n
