Vue.component('nav-menu', {
    template: `
    <div class="tabs is-centered is-fullwidth">
    <ul>
      <li class="is-active"><a>Pilots</a></li>
      <li><a>Airplanes</a></li>
      <li><a>Airports</a></li>
      <li><a>Flights</a></li>
    </ul>
  </div>
    `
})

Vue.component('page-title', {
    template: `
    <div class="hero is-info has-text-centered">
    <div class="hero-body">
        <div class="container">
            <h1 class="title">
                Pilots
            </h1>
        </div>
    </div>
</div>
    `
})