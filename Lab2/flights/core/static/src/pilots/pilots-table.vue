<template>
      <table class="table">
        <thead>
            <th>First Name</th>
            <th>Last Name</th>
            <th>On duty from</th>
            <th>Remove</th>
        </thead>
        <tbody>
            <tr v-for='pilot in pilots' :key="pilot.id">
                <td>{{pilot.firstname}}</td>
                <td>{{pilot.lastname}}</td>
                <td>{{pilot.starting_date}}</td>
                <td><button class="button is-danger" @click="remove(pilot.id)">Remove</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    export default {
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
};
</script>

<style>

</style>

