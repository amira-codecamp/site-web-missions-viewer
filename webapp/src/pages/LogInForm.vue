
<template>
    <div class="columns">
        <div class="column is-6 is-offset-3">

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
import employeesservice from '@/services/employeesservice'
import transportsservice from '@/services/transportsservice'

export default {
    name: 'LogInForm',
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

                const response0 = await tripsservice.trips.fetchTrips(access);
                this.$store.dispatch('setTrips', response0.trips);

                let transports = [];
                let employees = [];
                let missions = [];

                try {
                    const response1 = await transportsservice.fetchTransports(access);
                    transports = response1.transports;

                    const response2 = await employeesservice.fetchEmployees(access);
                    employees = response2.employees;

                    const response3 = await tripsservice.missions.fetchMissions(access);
                    missions = response3.missions;

                    this.$store.dispatch('setIsManager');
                } catch (error) {
                    console.warn('Erreur lors du chargement :', error);
                }

                this.$store.dispatch('setTransports', transports);
                this.$store.dispatch('setEmployees', employees);
                this.$store.dispatch('setMissions', missions);

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