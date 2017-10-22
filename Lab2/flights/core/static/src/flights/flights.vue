<template>
<div>
<div class="container ids">
    <button class="button is-primary is-large new-flight" @click="addFlightModal = true">
        New
    </button>
    <div class="card">
    <header class="card-header">
        <p class="card-header-title">
        Component
        </p>
        <a href="#" class="card-header-icon" aria-label="more options" @click="toggle()">
        <span class="icon">
            <i class="fa fa-angle-down" aria-hidden="true" v-if="isOpen"></i>
            <i class="fa fa-angle-up" aria-hidden="true" v-if="!isOpen"></i>
        </span>
        </a>
    </header>
    <transition name="slide">
        <div v-if="isOpen" class="card-content-wrapper">
        <div class="card-content">
            <div class="content">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus nec iaculis mauris.
            <a href="#">@bulmaio</a>. <a href="#">#css</a> <a href="#">#responsive</a>
            <br>
            <time datetime="2016-1-1">11:09 PM - 1 Jan 2016</time>
            </div>
        </div>
        <footer class="card-footer">
            <a href="#" class="card-footer-item">Save</a>
            <a href="#" class="card-footer-item">Edit</a>
            <a href="#" class="card-footer-item">Delete</a>
        </footer>
        </div>
    </transition>
    </div>
</div>
<add-flight-modal v-if="addFlightModal" @cancel="addFlightModal = false"></add-flight-modal>
</div>
</template>
<script>
import AddFlightModal  from './add-flight-modal.vue';
export default {
    components: {AddFlightModal},
    data: function() {
        return {
            isOpen: true,
            addFlightModal: false
        }
    },
    methods: {
        toggle() {
            this.isOpen = !this.isOpen;
        }
    }
}
</script>
<style>
.card-content-wrapper {
    max-height: 1000px;
}
.slide-enter-active {
  transition: all .5s cubic-bezier(0.55, 0.085, 0.68, 0.53)
}

.slide-leave-active {
  transition: all .55s cubic-bezier(0.25, 0.46, 0.45, 0.94)
}

.slide-enter, .slide-leave-to {
  max-height: 0;
  opacity: 0;
}

.new-flight {
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: 25px;
}
</style>
