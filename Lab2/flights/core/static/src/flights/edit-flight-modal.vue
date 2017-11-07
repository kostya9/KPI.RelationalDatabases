<template>
<div class="modal is-active">
    <div class="modal-background" @click="cancel()"></div>
    <div class="modal-card flight-modal">
        <header class="modal-card-head has-text-centered">
            <p class="modal-card-title">Edit Flight</p>
            <button class="delete" aria-label="close" @click="cancel()"></button>
        </header>
        <section class="modal-card-body">
            <form class="form">
                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label">Pilot</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <div class="select">
                                    <select v-model="flight.pilot" v-validate="{required: true}">
                                        <option value="">Select Pilot</option>
                                        <option v-for="pilot in pilots" :key="pilot.id" :value="pilot">{{pilot.firstname + " " + pilot.lastname}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label">Airplane</label>
                    </div>
                    <div class="field-body">
                        <div class="field">

                            <div class="control">
                                <div class="select">
                                    <select v-model="flight.airplane" v-validate="{required: true}">
                                        <option value="">Select Airplane</option>
                                        <option v-for="airplane in airplanes" :key="airplane.id" :value="airplane">{{airplane.modelname}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label">Departure</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <div class="select">
                                    <select  :required="true" v-model="flight.departureAirport" v-validate="{required: true}">
                                        <option v-for="airport in departureAirports"
                                         :key="airport.id" :value="airport">{{airport.code}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input type="datetime-local" class="input" name="departure-time" v-validate="{required: true}" id="" v-model="flight.departure_time">
                            </div>
                        </div>
                    </div>
                </div>
                <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label">Arrival</label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <div class="select">
                                    <select v-model="flight.arrivalAirport" v-validate="{required: true}">
                          <option v-for="airport in arrivalAirports" :key="airport.id" :value="airport" >{{airport.code}}</option>
                      </select>
                                </div>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input type="datetime-local" class="input" name="arrival-time" v-model="flight.arrival_time" v-validate="{required: true}">
                            </div>
                        </div>
                    </div>
                </div>
                 <p class="help is-danger is-large" v-if="$validator.errors.any()">Please, select all fields</p>
            </form>
        </section>
        <footer class="modal-card-foot">
            <button class="button is-success" :disabled="$validator.errors.any()" @click="onEdit()">Edit</button>
            <button class="button" @click="cancel()">Cancel</button>
        </footer>
    </div>
</div>
</template>
<script>
export default {
    props: ['actionName', 'flight'],
  methods: {
    cancel() {
      this.$emit("cancel");
    },
    onEdit() {
        this.$emit('edit')
    }
  },
  mounted() {
    if (this.$store.state.pilots.length == 0)
      this.$store.dispatch("fetch_pilots");

    if (this.$store.state.airplanes.length == 0)
      this.$store.dispatch("fetch_airplanes");

    if (this.$store.state.airports.length == 0)
      this.$store.dispatch("fetch_airports");
  },
  computed: {
    pilots() {
      return this.$store.state.pilots;
    },
    airplanes() {
      return this.$store.state.airplanes;
    },
    airports() {
      return this.$store.state.airports;
    },
    departureAirports() {
      return this.airports.filter(a => a.id != this.flight.arrivalAirport.id);
    },
    arrivalAirports() {
      return this.airports.filter(a => a.id != this.flight.departureAirport.id);
    }
  }
};
</script>
<style>
.flight-modal.modal-card {
}
</style>
