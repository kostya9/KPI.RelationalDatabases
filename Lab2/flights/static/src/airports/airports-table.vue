<template>
  <table class="table">
      <thead>
          <th>Name</th>
          <th>Code</th>
          <th>City</th>
          <th>Remove</th>
      </thead>
      <tbody>
          <tr v-for="airport in airports" :key="airport.id">
              <td>{{airport.name}}</td>
              <td>{{airport.code}}</td>
              <td>{{airport.city}}</td>
              <td><button class="button is-danger" @click="remove(airport.id)">Remove</button></td>
          </tr>
      </tbody>
  </table>
</template>
<script>
    export default {
        props: ['airports'],
        methods: {
            remove(id) {
                this.$emit('remove', id)
            }
        }
    }
</script>