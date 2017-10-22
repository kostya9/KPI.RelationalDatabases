import Pilots from './pilots/pilots.vue';
import Airplanes from './airplanes/airplanes.vue';
import Airports from './airports/airports.vue';
import Flights from './flights/flights.vue';

import store from './store'
import Vuex from 'vuex';

import PageTitle from './shared/page-title.vue';
import NavMenu from './shared/nav-menu.vue';
import VueRouter from 'vue-router';
import css from './styles.css';

const routes = [
    {path: '/', redirect: '/pilots'},
    {path: '/pilots', component: Pilots, name: 'Pilots'},
    {path: '/airplanes', component: Airplanes, name: 'Airplanes'},
    {path: '/airports', component: Airports, name: 'Airports'},
    {path: '/flights', component: Flights, name: 'Flights'},
]

const router = new VueRouter({
    routes, // short for `routes: routes`,
    mode: 'history'
  })

Vue.use(VeeValidate);


var app = new Vue({
    router,
    store,
    template: `
    <div>
    <page-title>{{title}}</page-title>
    <nav-menu></nav-menu>
    <transition name="appear">
    <router-view class="route"></router-view>
    </transition>
    </div>
    `,
    data: {
        transitionName: 'slide-right'
    },
    computed: {
        title() {
            return this.$route.name
        }
    },
    created() {
        this.$store.dispatch('fetch_airports')
        this.$store.dispatch('fetch_pilots')
        this.$store.dispatch('fetch_airplanes')
        this.$store.dispatch('fetch_flights')
    },
    el: '#root',
    components: {Pilots, PageTitle, NavMenu},
    watch: {
        '$route' (to,from) {
            let idxFrom = routes.findIndex(i => from.path == i.path)
            let idxTo = routes.findIndex(i => to.path == i.path)
            console.log({idxFrom, idxTo})
            this.transitionName = idxFrom < idxTo ? 'slide-left' : 'slide-right';
        }
    }
})