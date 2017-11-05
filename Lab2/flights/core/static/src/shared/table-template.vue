<template>
<span>
<div class="wrapper">
        <div class="table-wrapper">
        <div class="table-top-buttons">
            <button class="button is-info" href="importUrl">
                <span>Import</span>
                <input type="file" @change="fileChange($event)">
            </button>
            <a class="button is-info" :href="exportUrl">
                <span>Export</span>
            </a>
        </div>
      <table class="table">
        <thead>
            <th v-for="col in columnDefs" :key="col.name">{{col.name}}</th>
        </thead>
        <tbody>
            <tr v-for='row in rows' :key="row.id">
                <td v-for="col in columnDefs" :key="col.name">{{col.getValue(row)}}</td>
                <td><button class="button is-danger" @click="remove(row.id)">Remove</button></td>
            </tr>
        </tbody>
    </table>
        </div>
</div>
</span>
</template>

<script>
import axios from 'axios';
    export default {
    props: ['rows', 'exportUrl', 'importUrl', 'columnDefs'],
    data: function() {
        return {
            removeActive: false,
            curRemoveId: 0
        }
    },
    methods: {
        import() {
            this.$emit('import')
        },
        remove(id) {
            this.$emit('remove', id)
        },
        fileChange(event) {
            let file = event.target.files[0]
            if(file == null)
                return;

            let data = new FormData()
            data.append('file', file)
            axios.post(this.importUrl, data)
                .then(() => {
                    this.$emit('import')
                })

        }
    }
};
</script>

<style scoped>
input[type=file] {
    position: absolute;
    height: 100%;
    top: 0;
    right: 0;
    margin: 0;
    padding: 0;
    font-size: 20px;
    cursor: pointer;
    opacity: 0;
    filter: alpha(opacity=0);
}

    .wrapper {
        display: flex;
        justify-content: center;
        align-content: center;
        align-items: center;
        flex-direction: column;
    }

    .table-top-buttons {
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
    }
</style>

