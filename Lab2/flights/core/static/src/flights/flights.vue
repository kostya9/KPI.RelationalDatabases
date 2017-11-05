<template>
<div>
<div class="container">
    <button class="button is-primary is-large new-flight" @click="addFlightModal = true">
        New
    </button>
    <div class="card" :class="{'is-open': isOpen(flight)}" v-for="flight in flights" :key="flight.id">
    <header class="card-header">
        <div class="card-header-title">
            <nav class="level">
                <div class="level-item has-text-centered">
                    <p class="heading">{{flight.departure_time | datetime}}</p>
                </div>
                <div class="level-item has-text-centered">
                    <p class="title">{{getAirportDepartureCode(flight)}} > {{getAirportArrivalCode(flight)}}</p>
                </div>
                <div class="level-item has-text-centered">
                    <p class="heading">{{flight.arrival_time | datetime}}</p>
                </div>
            </nav>
        </div>
        <a class="card-header-icon" aria-label="more options" @click="toggle(flight)">
        <span class="icon">
            <i class="fa fa-angle-down" aria-hidden="true" v-if="isOpen(flight)"></i>
            <i class="fa fa-angle-up" aria-hidden="true" v-if="!isOpen(flight)"></i>
        </span>
        </a>
    </header>
    <transition name="slide">
        <div v-if="isOpen(flight)" class="card-content-wrapper">
            <div class="card-content">
                <div class="content">
                The plane takes off at the {{getAirportById(flight.departure_airport_id).name}} and lands at {{getAirportById(flight.arrival_airport_id).name}}
                <br/>
                <br/>
                {{getPilot(flight).firstname}} {{getPilot(flight).lastname}} will perform the flight. The pilot has {{getPilotExperience(flight)}} years of experience.
                <br/>
                <br/>
                The vehicle model's name is {{getAirplane(flight).modelname}}. The plane is {{getAirplaneAge(flight)}} years old.
                </div>
            </div>
            <footer class="card-footer">
                <a href="#" class="card-footer-item">Edit</a>
                <a href="#" class="card-footer-item">Delete</a>
            </footer>
        </div>
    </transition>
    </div>
</div>
<add-flight-modal v-if="addFlightModal" @ok="addFlight" @cancel="addFlightModal = false"></add-flight-modal>
</div>
</template>
<script>
import AddFlightModal  from './add-flight-modal.vue';
import axios from 'axios';
export default {
    components: {AddFlightModal},
    data: function() {
        return {
            addFlightModal: false,
            openFlights: []
        }
    },
    filters: {
        datetime(dateText) {
            let date = new Date(dateText)
            return date.toLocaleString()
        }
    },
    mounted() {
        if(this.$store.state.flights.length == 0)
            this.$store.dispatch('fetch_flights')
    },
    computed: {
        flights() {
            return this.$store.state.flights;
        }
    },
    methods: {
        toggle(flight) {
            let index = this.openFlights.indexOf(flight.id);
            if(index < 0)
                this.openFlights.push(flight.id);
            else
                this.openFlights.splice(index, 1);
        },
        addFlight(flight) {
            let url = '/api/flights'
            axios.post(url, flight)
                .then(response => {
                    this.$store.dispatch('fetch_flights');
                })
            this.addFlightModal = false;
        },
        isOpen(flight) {
            return this.openFlights.some(id => id == flight.id);
        },
        getAirportById(id) {
            return this.$store.state.airports.find(a => a.id == id)
        },
        getAirportDepartureCode(flight) {
            return this.getAirportById(flight.departure_airport_id).code
        },
        getAirportArrivalCode(flight) {
            return this.getAirportById(flight.arrival_airport_id).code
        },
        getPilot(flight) {
            return this.$store.state.pilots.find(p => p.id == flight.pilot_id)
        },
        getPilotExperience(flight) {
            let pilot = this.getPilot(flight)
            let date = new Date(pilot.starting_date)
            return new Date().getFullYear() - date.getFullYear()
        },
        getAirplane(flight) {
            return this.$store.state.airplanes.find(a => a.id == flight.airplane_id)
        },
        getAirplaneAge(flight) {
            let airplane = this.getAirplane(flight)
            let date = new Date(airplane.builddate)
            return new Date().getFullYear() - date.getFullYear()
        }
    }
}
</script>
<style>

.card {
    margin-bottom: 0px;
    margin-top: 0px;
    transition: all .5s cubic-bezier(0.55, 0.085, 0.68, 0.53)
}

.card.is-open {
    margin-top: 100px;
    margin-bottom: 100px;
}

.card:first-of-type {
    margin-top: 0px;
}

.card-content-wrapper {
    max-height: 1000px;
    box-sizing: border-box;

}
.slide-enter-active {
  transition: all .5s cubic-bezier(0.55, 0.085, 0.68, 0.53)
}

.slide-leave-active {
  transition: all .55s cubic-bezier(0.25, 0.46, 0.45, 0.94)
}

.slide-enter, .slide-leave-to {
  max-height: 0;
  margin-bottom: 0;
  margin-top: 0;
  opacity: 0;
}

.new-flight {
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: 25px;
}

.level {
    width: 100%;
}
</style>
