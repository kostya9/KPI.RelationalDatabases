<template>
      <table class="table">
        <thead>
            <th>Model Name</th>
            <th>Build Date</th>
            <th>Remove</th>
        </thead>
        <tbody>
            <tr v-for='airplane in airplanes' :key="airplane.id">
                <td>{{airplane.modelname}}</td>
                <td>{{airplane.builddate }}</td>
                <td><button class="button is-danger" @click="remove(airplane.id)">Remove</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    export default {
    props: ['airplanes'],
    data: function() {
        return {
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

