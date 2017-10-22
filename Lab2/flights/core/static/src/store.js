import Vuex from 'vuex';
import axios from 'axios';

const store = new Vuex.Store({
    state: {
        airplanes: [],
        pilots: [],
        airports: []
    },
    mutations: {
        replace_pilots(state, pilots) {
            state.pilots = pilots;
        },
        replace_airplanes(state, airplanes) {
            state.airplanes = airplanes
        },
        replace_airports(state, airports) {
            state.airports = airports;
        }
    },
    actions: {
        fetch_airplanes() {
            let url = '/api/airplanes'
            axios.get(url)
                .then(response => {
                    let airplanes = response.data
                    this.commit('replace_airplanes', airplanes)
                })
        },
        fetch_pilots() {
            let url = '/api/pilots'
            axios
                .get(url)
                .then((response) => {
                    let pilots = response.data
                    this.commit('replace_pilots', pilots)
                })
        },
        fetch_airports() {
            let url = '/api/airports'
            axios.get(url)
                .then(response => {
                    let airports = response.data;
                    this.commit('replace_airports', airports)
                })
        }
    }
})

export default store;