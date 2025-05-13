
<template>
    <div class="columns">
        <div class="column is-4 is-offset-4">

            <form @submit.prevent="submitForm">

                <div class="field mb-4">
                    <label>Login</label>
                    <div class="control">
                        <input type="text" class="input" v-model="login" required maxlength="50" placeholder="Enter your login">
                    </div>
                </div>

                <div class="field mb-4">
                    <label>Password</label>
                    <div class="control">
                        <input type="password" class="input" v-model="password" required placeholder="Enter your password">
                    </div>
                </div>

                <div class="notification is-danger mb-4" v-if="errors.length">
                    <p v-for="error in errors" :key="error">{{ error }}</p>
                </div>

                <div class="field mb-4">
                    <div class="control">
                        <button class="button is-dark">Log In</button>
                    </div>
                </div>

            </form>
        </div>

    </div>
</template>


<script>
import authservice from '@/services/authservice';
import tripsservice from '@/services/tripsservice';

export default {
    name: 'LogIn',
    data() {
        return {
            login: '',
            password: '',
            errors: [],
        };
    },
    mounted() {
        document.title = "Log In | LIPN-carbon";
    },
    methods: {
        async submitForm() {
            this.errors = [];
            
            if (!this.login || !this.password) {
                this.errors.push('Both login and password are required.');
                return;
            }

            try {
                const credentials = { login: this.login, password: this.password };
                this.$store.dispatch('setUser', this.login);
                const { access, refresh } = await authservice.login(credentials);
                const trips = await tripsservice.fetchTrips(access);
                this.$store.dispatch('setTrips', trips);
                this.$router.push('/dashboard');

            } catch (error) {
                if (error.response) {
                    for (const property in error.response.data) {
                        this.errors.push(`${property}: ${error.response.data[property]}`);
                    }
                } else {
                    this.errors.push('Something went wrong. Please try again');
                }
                console.error(error);
            }
        }
    }
};
</script>