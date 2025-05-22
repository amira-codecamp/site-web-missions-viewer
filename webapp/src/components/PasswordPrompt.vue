
<template>
    <div v-if="visible" class="modal is-active">
      <div class="modal-background"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">Enter your password to confirm</p>
          <button class="delete" aria-label="close" @click="cancel"></button>
        </header>
        <section class="modal-card-body">
          <input
            class="input"
            type="password"
            v-model="password"
            placeholder="Password"
            @keyup.enter="confirm"
            autofocus
          />
        </section>
        <footer class="modal-card-foot is-justify-content-flex-end">
          <button class="button is-dark" :disabled="!password" @click="confirm">
            Confirm
          </button>
        </footer>
      </div>
    </div>
</template>
  
<script>
  export default {
    data() {
      return {
        visible: false,
        password: '',
        resolve: null,
      };
    },
    methods: {
      open() {
        this.password = '';
        this.visible = true;
        return new Promise((resolve) => {
          this.resolve = resolve;
        });
      },
      confirm() {
        if (!this.password) return;
        this.visible = false;
        this.resolve(this.password);
      },
      cancel() {
        this.visible = false;
        this.resolve(null);
      },
    },
  };
</script>  