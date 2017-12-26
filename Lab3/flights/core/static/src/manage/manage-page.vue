<template>
  <div class="wrapper">
      <div class="field" @click="onVerifyChange()">
        <input type="checkbox" class="switch is-info" :checked="verify">
        <label for="switchVerify">Verify flight dates</label>
      </div>
    <div class="is-divider" data-content=""></div>
      <div class="field" @click="onRemoveChange()">
        <input type="checkbox" class="switch is-info" :checked="remove">
        <label for="switchRemove">Raise events to remove all data each week</label>
      </div>
      <div class="field is-horizontal">
                    <div class="field-label is-normal">
                        <label class="label">starting: </label>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <flat-pickr v-model="date" class="input" :config="config" :disabled="!remove" placeholder="Select time"></flat-pickr>
                            </div>
                        </div>
                    </div>
                    <div class="field-body">
                        <div class="field">
                            <div class="control">
                                <button class="button is-info" @click="onSave()" :disabled="!remove || !touched">Save</button>
                            </div>
                        </div>
                    </div>
                </div>

  </div>
</template>
<script>
import axios from 'axios';
import flatPickr from 'vue-flatpickr-component';
import 'flatpickr/dist/flatpickr.css';
export default {
    components: {flatPickr},
    data:  function() {
        return {
            verify: false,
            remove: false,
            config: {
                enableTime: true,
                minuteIncrement: 1
            },
            date: new Date(),
            initial_date: null
        }
    },
    methods: {
        onVerifyChange: function() {
            let newValue = !this.verify;
            axios.post('/api/trigger', newValue)
            .then(() => {
                this.verify = newValue;
            })
        },
        onRemoveChange: function() {
            let newValue = !this.remove;
            axios.post('/api/event', {enabled: newValue, date: this.date})
            .then(() => {
                this.remove = newValue;
            })
        },
        onSave: function() {
            axios.post('/api/event', {enabled: true, date: this.date})
                .then(() => {
                    this.initial_date = this.date
                })
        }
    },
    mounted: function () {
        axios.get('/api/trigger')
            .then((result) => {
                this.verify = result.data;
            })
        axios.get('/api/event')
            .then((result) => {
                this.remove = result.data.enabled;
                let date = result.data.start_date
                this.initial_date = date.slice(0, date.length - 3) // remove seconds
                this.date = this.initial_date
            })
    },
    computed: {
        touched: function() {
            console.log(this)
            return this.initial_date !== this.date;
        },
        starting_date() {
            if(!this.remove)
                return "today";
            else
                return this.initial_date;
        }
    }
}
</script>
<style scoped>
    .wrapper {
        display: flex;
        justify-content: center;
        align-content: center;
        align-items: center;
        flex-direction: column;
    }
    .is-divider {
        min-width: 600px;
    }
    label {
          -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome and Opera */
    }

    .field-body {
        margin-left: 10px;
    }
</style>
