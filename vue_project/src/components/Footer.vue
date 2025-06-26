<template>
  <footer class="footer has-background-light py-3">
    <div class="fixed-grid has-4-cols">
      <div class="grid">
        <div class="cell">
          <img width="150" src="@/assets/USPN-logo.png" alt="USPN" />
        </div>

        <div class="cell">
          <p class="is-flex is-flex-direction-column">
            <span>LIPN, UMR CNRS 7030</span>
            <span>Sorbonne Paris Nord University</span>
            <span>99, Avenue Jean-Baptiste Clément</span>
            <span>93430 Villetaneuse</span>
          </p>
        </div>

        <div class="cell">
          <p class="is-flex is-flex-direction-column">
            <span>Contact :</span>
            <span>Tel. : 01 49 40 35 90</span>
            <span>Fax : 01 48 26 07 12</span>
            <span><a href="mailto:contact@lipn.univ-paris13.fr">contact@lipn.univ-paris13.fr</a></span>
          </p>
        </div>

        <div class="cell">
          <img width="80" src="@/assets/CNRS_logo.png" alt="CNRS" />
          <img width="80" src="@/assets/LIPN-blue-logo.png" alt="LIPN" />
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
defineOptions({
  name: 'Footer',
})
</script>
