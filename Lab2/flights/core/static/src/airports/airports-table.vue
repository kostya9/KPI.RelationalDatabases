<template>
<table-template class="airports-table-wrapper" @import="onImport()" :rows="airports" :columnDefs="columnDefs" @remove="remove" importUrl='/api/airports/import' exportUrl="/api/airports/export">
</table-template>
</template>
<script>
import TableTemplate from './../shared/table-template.vue';
    export default {
        components: {TableTemplate},
        props: ['airports'],
        data: function (){
            return {
                columnDefs: [{
                    name: 'Name',
                    getValue: (a) => a.name
                    }, {
                        name: 'Code',
                        getValue: (a) => a.code
                    }, {
                        name: 'City',
                        getValue: (a) => a.city
                    }
                ]
            }
        },
        methods: {
            remove(id) {
                this.$emit('remove', id)
            },
            onImport() {
                this.$store.dispatch('fetch_airports')
            }
        }
    }
</script>
<style>
.airports-table-wrapper th:first-of-type {
    min-width: 100px;
} 
</style>
