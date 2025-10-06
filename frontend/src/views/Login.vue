<template>
  <div class="auth-page d-flex align-items-center justify-content-center">
    <div class="form-box p-4 p-md-5">
      <h2 class="text-white text-center mb-4">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="email"
            required
          />
        </div>

        <div class="mb-4">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-100 btn-lg">Login</button>
      </form>
      <p class="mt-4 text-center bottom-link">
        Don't have an account?
        <router-link to="/register">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import jwtDecode from 'jwt-decode';
import api from '../services/api';

const router = useRouter();

const email = ref('');
const password = ref('');

const handleLogin = async () => {
  try {
    const response = await api.post('/login', {
      email: email.value,
      password: password.value,
    });

    const { access_token } = response.data;
    localStorage.setItem('accessToken', access_token);

    const userData = jwtDecode(access_token);
    
    // --- THIS IS THE FIX ---
    // Change 'userData.identity.role' to 'userData.sub.role'
    const userRole = userData.sub.role;

    alert('Login successful!');

    if (userRole === 'admin') {
      router.push('/admin/dashboard');
    } else {
      router.push('/dashboard');
    }

  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert('Login failed: Invalid email or password.');
    } else {
      alert('An error occurred during login.');
      console.error(error);
    }
  }
};
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(45deg, #240046 0%, #5a189a 100%);
  color: white;
}

.form-box {
  width: 100%;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.form-label {
  color: rgba(255, 255, 255, 0.8);
}

.form-control {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.form-control:focus {
  background-color: rgba(0, 0, 0, 0.3);
  border-color: #ff758f;
  color: white;
  box-shadow: none;
}

.btn-primary {
  background-color: #ff4d6d;
  border-color: #ff4d6d;
  font-weight: bold;
}

.btn-primary:hover {
  background-color: #ff758f;
  border-color: #ff758f;
}

.bottom-link {
  color: rgba(255, 255, 255, 0.7);
}

.bottom-link a {
  color: #ffca3a;
  text-decoration: none;
  font-weight: bold;
}

.bottom-link a:hover {
  text-decoration: underline;
}
</style>