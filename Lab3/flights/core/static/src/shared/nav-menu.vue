<template>
    <div class="tabs is-centered is-fullwidth">
        <ul>
            <router-link tag="li" to="/pilots" active-class="is-active">
                <a>Pilots</a>
            </router-link>
            <router-link tag="li" to="/airplanes" active-class="is-active">
                <a>Airplanes</a>
            </router-link>
            <router-link tag="li" to="/airports" active-class="is-active">
                <a>Airports</a>
            </router-link>
            <router-link tag="li" to="/flights" active-class="is-active">
                <a>Flights</a>
            </router-link>
            <router-link tag="li" to="/manage" active-class="is-active">
                <a>Manage</a>
            </router-link>
        </ul>
    </div>
</template>

<script>
export default {

}
</script>
