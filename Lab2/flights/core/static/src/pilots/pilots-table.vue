<template>
    <table-template @import="onImport()" :rows="pilots" :columnDefs="columnDefs" @remove="remove" exportUrl="/api/pilots/export" importUrl="/api/pilots/import">
    </table-template>
</template>

<script>
import TableTemplate from './../shared/table-template.vue';
    export default {
    components: {TableTemplate},
    props: ['pilots'],
    data: function() {
        return {
            columnDefs: [{
                name: 'First Name',
                getValue: (p) => p.firstname
            }, {
                name: 'Last Name',
                getValue: (p) => p.lastname,
            }, {
                name: 'On duty from',
                getValue: (p) => p.starting_date
            }
            ]
        }
    },
    methods: {
        remove(id) {
            this.$emit('remove', id)
        },
        onImport() {
            this.$store.dispatch('fetch_pilots')
        }
    }
};
</script>

<style>

</style>

