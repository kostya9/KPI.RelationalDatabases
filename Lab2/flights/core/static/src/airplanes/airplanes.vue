<template>
    <section class="container ids">
        <nav class="is-centered level controls">
            <level-control>
                <input class="input" type="text" placeholder="Model Name" v-model="modelname">
            </level-control>
            <level-control>

            </level-control>
            <level-control>
                <div class="field is-horizontal build-range">
                    <div class="field-label">
                        <label class="label">Build range</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <p class="control">
                            <input class="input" placeholder="123" type="date" name="from" v-model="buildrangeStart">
                            </p>
                        </div>
                        <div class="field">
                            <input class="input" placeholder="123" type="date" name="from" v-model="buildrangeEnd">
                        </div>
                    </div>
                </div>
            </level-control>
            <level-control>
                <button class="button is-default" @click="search()">
                    Search
                </button>
            </level-control>
            <level-control>
                <button class="button is-default" @click="reset()">
                    Reset
                </button>
            </level-control>
        </nav>
        <airplanes-table @remove="remove" class="is-centered" :airplanes="airplanes">
        </airplanes-table>
    </section>
</template>

<script>
import LevelControl from './../shared/level-control.vue';
import AirplanesTable from './airplanes-table.vue';
import axios from 'axios';
export default {
    components: { AirplanesTable, LevelControl },
    mounted() {
        if (this.$store.state.airplanes.length == 0)
            this.$store.dispatch('fetch_airplanes')
    },
    data: function(){
        return {
            queryAirplanes: null,
            buildrangeStart: '1900-01-01',
            buildrangeEnd: new Date().toISOString().slice(0, 10),
            modelname: ''
        }
    },
    methods: {
        search() {
            let url = '/api/airplanes/search';
            let params = {buildrangeStart: this.buildrangeStart, buildrangeEnd: this.buildrangeEnd, modelname: this.modelname}
            axios.get(url, {params})
                .then(response => {
                    this.queryAirplanes = response.data;
                })

        },
        remove(id) {
            let url = '/api/airplanes/' + id;
            axios.delete(url)
                .then(response => {
                    this.$store.dispatch('fetch_airplanes')
                    this.$store.dispatch('fetch_flights')
                })
        },
        reset() {
            this.queryAirplanes = null;
            this.buildrangeStart = '1900-01-01';
            this.buildrangeEnd = new Date().toISOString().slice(0, 10);
            this.modelname = '';
        }
    },
    computed: {
        airplanes() {
            return this.queryAirplanes || this.$store.state.airplanes;
        }
    }
}  
</script>

<style>
.build-range .label {
    width: 100px;
    transform: translateY(25%);
}

.build-range .field-label  {
    margin-right: 1rem;
}
</style>
