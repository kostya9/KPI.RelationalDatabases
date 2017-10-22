<template>
<div class="modal is-active">
    <div class="modal-background" @click="cancel()"></div>
    <div class="modal-card flight-modal">
        <header class="modal-card-head has-text-centered">
            <p class="modal-card-title">New Flight</p>
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
                                    <select v-model="pilot" v-validate="{required: true}">
                                        <option value="">Select Pilot</option>
                                        <option v-for="pilot in pilots" :key="pilot.id" :value="pilot">{{pilot.name}}</option>
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
                                    <select v-model="airplane" v-validate="{required: true}">
                                        <option value="">Select Airplane</option>
                                        <option v-for="airplane in airplanes" :key="airplane.id" :value="airplane">{{airplane.name}}</option>
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
                                    <select v-model="departureAirport" v-validate="{required: true}">
                                        <option value="">Select Airport</option>
                                        <option v-for="airport in departureAirports" :key="airport.id" :value="airport">{{airport.name}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input type="datetime-local" class="input" name="departure-time" v-validate="{required: true}" id="" v-model="departureTime">
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
                                    <select v-model="arrivalAirport" v-validate="{required: true}">
                          <option value="">Select Airport</option>
                          <option v-for="airport in arrivalAirports" :key="airport.id" :value="airport">{{airport.name}}</option>
                      </select>
                                </div>
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input type="datetime-local" class="input" name="arrival-time" v-model="arrivalTime" v-validate="{required: true}">
                            </div>
                        </div>
                    </div>
                </div>
                 <p class="help is-danger is-large" v-if="$validator.errors.any()">Please, select all fields</p>
            </form>
        </section>
        <footer class="modal-card-foot">
            <button class="button is-success" :disabled="$validator.errors.any()" @click="ok()">Add</button>
            <button class="button" @click="cancel()">Cancel</button>
        </footer>
    </div>
</div>
</template>
<script>
export default {
  methods: {
    cancel() {
      this.$emit("cancel");
    },
    ok() {
      this.$validator.validateAll();

      if(this.$validator.errors.any())
          return false;

        console.log(this)
        this.$emit('ok', {
          pilot_id: this.pilot.id,
          airplane_id: this.airplane.id,
          departure_airport_id: this.departureAirport.id,
          arrival_airport_id: this.arrivalAirport.id,
          departure_time: this.departureTime, 
          arrival_time: this.arrivalTime
        })
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
  data: function() {
    return {
      pilot: "",
      airplane: "",
      departureAirport: "",
      arrivalAirport: "",
      departureTime: "",
      arrivalTime: ""
    };
  },
  computed: {
    pilots() {
      return this.$store.state.pilots.map(p => {
        return {
          id: p.id,
          name: p.firstname + " " + p.lastname
        };
      });
    },
    airplanes() {
      return this.$store.state.airplanes.map(a => {
        return {
          id: a.id,
          name: a.modelname
        };
      });
    },
    airports() {
      return this.$store.state.airports.map(a => {
        return {
          id: a.id,
          name: a.code
        };
      });
    },
    departureAirports() {
      if (!this.arrivalAirport) return this.airports;

      return this.airports.filter(a => a.id != this.arrivalAirport.id);
    },
    arrivalAirports() {
      if (!this.departureAirport) return this.airports;

      return this.airports.filter(a => a.id != this.departureAirport.id);
    }
  }
};
</script>
<style>
.flight-modal.modal-card {
}
</style>
