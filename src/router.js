import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home.vue'
import Players from './views/Players.vue'
import NotFound from './views/NotFound.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home', 
      meta: {layout: 'main-layout'},
      component: Home
    },
    {
      path: '/players/:id?',
      name: 'players',
      meta: {layout: 'main-layout'},
      component: Players
    },
    { path: '/404', meta: {layout: 'empty-layout'}, component: NotFound},
    { path: '*', redirect: '/404' }
  ]
})

export default router
