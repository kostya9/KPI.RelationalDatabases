

<template>
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
        <add-pilot-modal v-if="addPilotModalActive" @cancel="cancel()" @ok="ok"></add-pilot-modal>
    </section>
</template>

<script>
import LevelControl from './../shared/level-control.vue'
import PilotsTable from './pilots-table.vue'
import AddPilotModal from './add-pilot-modal.vue'
export default {
    components: {LevelControl, PilotsTable, AddPilotModal},
    data: function() {
        return {
            pilots: [],
            firstname: "",
            lastname: "",
            addPilotModalActive: false
        }
    },
    created() {
        this.search();
    },
    methods: {
        reset() {
            this.firstname = "",
                this.lastname = "",
                this.search()
        },
        search() {
            let url, params;
            if (this.firstname == "" && this.lastname == "") {
                url = "/api/pilots/"
                params = {}
            }
            else {
                url = "/api/pilots/search"
                params = { firstname: this.firstname, lastname: this.lastname }
            }
            axios
                .get(url, { params: params })
                .then((response) => {
                    this.pilots = response.data
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
                    this.search()
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
.is-centered {
    margin-left: auto;
    margin-right: auto;
}

.table td {
    vertical-align: middle;
}

.ids {
    position: relative;
    clear: both;
    zoom: 1;
}

.ids:after {
    visibility: hidden;
    display: block;
    content: "";
    clear: both;
    height: 0;
}

.controls {
    max-width: 1000px;
    padding: 25px;
    border-radius: 10px;
    background-color: lightblue;
}

.add-pilot .modal-card {
    width: 300px;
}
</style>
