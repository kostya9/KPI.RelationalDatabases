
Vue.use(VeeValidate);
Vue.component('add-pilot-modal', {
    template: `
    <div class="modal is-active add-pilot">
    <div class="modal-background" @click="cancel()"></div>
    <div class="modal-card" v-on:keyup.13="ok()">
      <header class="modal-card-head has-text-centered">
        <p class="modal-card-title">Add pilot</p>
        <button class="delete" aria-label="close" @click="cancel()"></button>
      </header>
      <section class="modal-card-body">
        <form class="form">
            <div class="field">
                <label class="label">First Name</label>
                <div class="control">
                    <input class="input" v-validate="{required: true}" :class="{'is-danger': errors.has('First Name')}" type="text" placeholder="First Name" name="First Name" v-model="firstname">
                </div>
                <p v-show="errors.has('First Name')" class="help is-danger">{{ errors.first('First Name') }}</p>
            </div>
            <div class="field">
                <label class="label">Last Name</label>
                <div class="control">
                    <input class="input" :class="{'is-danger': errors.has('Last Name')}" v-validate="{required: true}" type="text" placeholder="Last Name" name="Last Name" v-model="lastname">
                </div>
                <p v-show="errors.has('Last Name')" class="help is-danger">{{ errors.first('Last Name') }}</p>
            </div>
            <div class="field">
                <label class="label">Pilot License date</label>
                <div class="control">
                    <input class="input" :class="{'is-danger': errors.has('Pilot License date')}" v-validate="{required: true, date_format: 'YYYY-MM-DD'}" type="text" placeholder="YYYY-MM-DD" name="Pilot License date" v-model="startdate">
                </div>
                <p v-show="errors.has('Pilot License date')" class="help is-danger">{{ errors.first('Pilot License date') }}</p>
            </div>
        </form>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-info" @click="ok()" :disabled="$validator.errors.any()">Save changes</button>
        <button class="button" @click="cancel()">Cancel</button>
      </footer>
    </div>
  </div>
    `,
    methods: {
        cancel() {
            this.$emit('cancel')
        },
        ok() {
            this.$validator.validateAll();

            if(this.$validator.errors.any())
                return false;

            this.$emit('ok', {firstname: this.firstname, lastname: this.lastname, startdate: new Date(this.startdate)})
        }
    },
    data: function(){
        a = this
        return {
            firstname: "",
            lastname: "",
            startdate: ""
        }
    }
})


Vue.component('pilots-table', {
    template: `
    <table class="table">
        <thead>
            <th>First Name</th>
            <th>Last Name</th>
            <th>On duty from</th>
            <th>Remove</th>
        </thead>
        <tbody>
            <tr v-for='pilot in pilots'>
                <td>{{pilot.firstname}}</td>
                <td>{{pilot.lastname}}</td>
                <td>{{pilot.starting_date}}</td>
                <td><button class="button is-danger" @click="remove(pilot.id)">Remove</button></td>
            </tr>
        </tbody>
    </table>
    `,
    props: ['pilots'],
    data: function() {
        return {
        }
    },
    filters: {
        date(date) {
            return date.toLocaleDateString();
        }
    },
    methods: {
        remove(id) {
            this.$emit('remove', id)
        }
    }
})

Vue.component('level-control', {
    template: `
    <div class="level-item">
    <div class="field">
        <p class="control">
            <slot></slot>
        </p>
    </div>
</div>
    `
})

Vue.component('pilots', {
    template: `
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
                    <button @click="reset()"  class="button is-default">
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
        <add-pilot-modal v-if="addPilotModalActive" 
            @cancel="cancel()" 
            @ok="ok"></add-pilot-modal>
    </section>
    `,
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
            if(this.firstname == "" && this.lastname == "") {
                url = "/api/pilots/"
                params = {}
            }
            else {
                url = "/api/pilots/search"
                params = {firstname: this.firstname, lastname: this.lastname}
            }
            axios
                .get(url, {params: params})
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
})

var app = new Vue({
    el: '#root',



})