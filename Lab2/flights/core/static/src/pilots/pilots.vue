<template>
<span>
    <section class="container ids">
        <nav class="level is-centered controls" v-on:keyup.13="search()">
            <div class="level-left">
                <level-control>
                    <input class="input" type="text" placeholder="First Name" v-model="firstname">
                </level-control>
                <level-control>
                    <input class="input" type="text" placeholder="Last Name" v-model="lastname">
                </level-control>
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
            <div class="level-right">
                <level-control>
                    <button class="button is-info" @click="addPilotModalActive = !addPilotModalActive">
                        New Pilot
                    </button>
                </level-control>
            </div>
        </nav>
        <pilots-table @remove="remove" class="is-centered" :pilots="pilots"></pilots-table>
    </section>
    <add-pilot-modal v-if="addPilotModalActive" @cancel="cancel()" @ok="ok"></add-pilot-modal>
</span>
</template>

<script>
import LevelControl from './../shared/level-control.vue'
import PilotsTable from './pilots-table.vue'
import AddPilotModal from './add-pilot-modal.vue'
import axios from 'axios';

export default {
    components: {LevelControl, PilotsTable, AddPilotModal},
    data: function() {
        return {
            queryPilots: null,
            firstname: "",
            lastname: "",
            addPilotModalActive: false
        }
    },
    created() {
        if(this.$store.state.pilots.length == 0)
            this.$store.dispatch('fetch_pilots')
    },
    computed: {
        pilots() {
            return this.queryPilots || this.$store.state.pilots;
        }
    },
    methods: {
        reset() {
            this.firstname = "",
            this.lastname = "",
            this.queryPilots = null;
        },
        search() {
            let url = "/api/pilots/search"
            let params = { firstname: this.firstname, lastname: this.lastname }
            axios
                .get(url, { params: params })
                .then((response) => {
                    this.queryPilots = response.data;
                })
        },
        remove(id) {
            let url = '/api/pilots/' + id;
            axios
                .delete(url)
                .then(() => {
                    this.search()
                })
        },
        cancel() {
            this.addPilotModalActive = false;
        },
        addPilot(pilot) {
            let url = '/api/pilots/';
            return axios
                .post(url, pilot)
                .then(() => {
                    this.$store.dispatch('fetch_pilots')
                });
        },
        ok(pilot) {
            this.addPilot(pilot)
                .then(() => this.search())
            this.cancel()
        }
    }
};
</script>

<style>
.add-pilot .modal-card {
    width: 300px;
}
</style>
