
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
                <td><button class="button is-danger">Remove</button></td>
            </tr>
        </tbody>
    </table>
    `,
    data: function() {
        return {
            pilots: [
            ]
        }
    },
    filters: {
        date(date) {
            return date.toLocaleDateString();
        }
    },
    created() {
        this.loadPilots();
    },
    methods: {
        loadPilots() {
            let url = "/api/pilots";
            axios.get(url)
                .then((response) => {
                    this.pilots = response.data;
                });
        }
    }
})

var app = new Vue({
    el: '#root'
})