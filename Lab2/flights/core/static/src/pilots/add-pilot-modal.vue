<template>
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
</template>

<script>
export default {
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
    data: function() {
        return {
            firstname: "",
            lastname: "",
            startdate: ""
        }
    }
};
</script>