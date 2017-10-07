import Pilots from './pilots/pilots.vue'

import PageTitle from './shared/page-title.vue'
import NavMenu from './shared/nav-menu.vue'
import VueRouter from 'vue-router'

const routes = [
    {path: '/pilots', component: Pilots, name: 'Pilots'},
    {path: '/airplanes', component: Pilots, name: 'Airplanes'},
    {path: '/airports', component: Pilots, name: 'Airports'},
    {path: '/flights', component: Pilots, name: 'Flights'}
]

const router = new VueRouter({
    routes, // short for `routes: routes`,
    mode: 'history'
  })

Vue.use(VeeValidate);

var app = new Vue({
    router,
    template: `
    <div>
    <page-title>{{title}}</page-title>
    <nav-menu></nav-menu>
    <router-view></router-view>
    </div>
    `,
    data: {
        
    },
    computed: {
        title() {
            return this.$route.name
        }
    },
    el: '#root',
    components: {Pilots, PageTitle, NavMenu}
})