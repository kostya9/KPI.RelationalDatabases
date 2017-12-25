<template>
<table-template @import="onImport()" :rows="airplanes" :columnDefs="columnDefs" @remove="remove" importUrl="/api/airplanes/import" exportUrl="/api/airplanes/export">
</table-template>
</template>

<script>
    import TableTemplate from './../shared/table-template.vue';
    export default {
    props: ['airplanes'],
    components: {TableTemplate},
    data: function() {
        return {
            columnDefs: [{
                    name: 'Model Name',
                    getValue: (a) => a.modelname
                }, {
                    name: 'Build Date',
                    getValue: (a) => a.builddate
                }
            ]
        }
    },
    methods: {
        remove(id) {
            this.$emit('remove', id)
        },
        onImport() {
            this.$store.dispatch('fetch_airplanes')
        }
    }
};
</script>