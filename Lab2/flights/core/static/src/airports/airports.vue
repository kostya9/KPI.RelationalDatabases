<template>
<span>
    <section class="container ids">
        <nav class="level is-centered controls" v-on:keyup.13="search()">
            <div class="level-left">
                <level-control>
                    <input class="input" type="text" placeholder="Name" v-model="name">
                </level-control>
                <level-control>
                    <input class="input" type="text" placeholder="Code" v-model="code">
                </level-control>
                <level-control>
                                <div class="select">
                        <select v-model="city" v-validate="{required: true}">
                          <option value="">Select City</option>
                          <option v-for="city in cities" :key="city" :value="city">{{city}}</option>
                      </select>
                            </div>
                </level-control>
            </div>
            <div class="level-right">
                <level-control>
                    <button @click="search()" class="button is-default">
                        Search
                    </button>
                </level-control>
                <level-control>
                    <button @click="reset()" class="button is-default">
                        Reset
                    </button>
                </level-control>
            </div>
        </nav>
        <airports-table @remove="remove" class="is-centered" :airports="airports"></airports-table>
    </section>
</span>
</template>

<script>
import AirportsTable from './airports-table.vue';
import LevelControl from './../shared/level-control.vue';
import axios from 'axios';

    export default {
        components: {AirportsTable, LevelControl},

        data: function() {
            return {
                name: '',
                code: '',
                city: '',
                queryAirports: null
            }
        },
        mounted: function() {
            if(this.$store.state.airports.length == 0)
                this.$store.dispatch('fetch_airports')
        },
        methods: {
            remove(id) {
                let url = '/api/airports/' + id
                axios.delete(url)
                    .then(response => {
                        this.$store.dispatch('fetch_airports')
                        this.$store.dispatch('fetch_flights')
                    })
            },
            reset() {
                this.queryAirports = null;
                this.name = '',
                this.code = '',
                this.city = ''
            },
            search() {
                let url = '/api/airports/search';
                let params = {name: this.name, code: this.code, city: this.city}
                axios.get(url, {params})
                    .then(response => {
                        this.queryAirports = response.data
                    })
            },

        },
        computed: {
            airports() {
                return this.queryAirports || this.$store.state.airports;
            },
            cities() {
                let allCities = this.$store.state.airports.map(a => a.city);
                return Array.from(new Set(allCities))
            }
        }
    }
</script>