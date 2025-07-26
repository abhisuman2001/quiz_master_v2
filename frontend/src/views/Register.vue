<template>
  <div class="auth-page d-flex align-items-center justify-content-center py-5">
    <div class="form-box p-4 p-md-5">
      <h2 class="text-white text-center mb-4">Create an Account</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="fullName" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="fullName" v-model="user.fullName" required />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input type="email" class="form-control" id="email" v-model="user.email" required />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input type="password" class="form-control" id="password" v-model="user.password" required />
        </div>

        <div class="mb-3">
          <label for="qualification" class="form-label">Qualification</label>
          <input type="text" class="form-control" id="qualification" v-model="user.qualification" />
        </div>

        <div class="mb-3">
          <label for="dob" class="form-label">Date of Birth</label>
          <input type="date" class="form-control" id="dob" v-model="user.dob" />
        </div>

        <button type="submit" class="btn btn-primary w-100 btn-lg">Register</button>
      </form>
      <p class="mt-4 text-center bottom-link">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { RouterLink, useRouter } from 'vue-router'; // 1. Import useRouter
import api from '../services/api'; // 2. Import the new api service

const router = useRouter(); // 3. Get the router instance


const user = ref({
  fullName: '',
  email: '',
  password: '',
  qualification: '',
  dob: '',
});

// 4. Make the function async to use await
const handleRegister = async () => {
  try {
    // 5. Send a POST request to the backend /register endpoint
    const response = await api.post('/register', user.value);

    // 6. Handle success
    console.log(response.data.msg); // "User registered successfully"
    alert('Registration successful! Please log in.');
    router.push('/login'); // Redirect to the login page

  } catch (error) {
    // 7. Handle errors (e.g., user already exists)
    if (error.response) {
      console.error('Registration failed:', error.response.data.msg);
      alert(`Registration failed: ${error.response.data.msg}`);
    } else {
      console.error('An error occurred:', error.message);
      alert('An error occurred during registration.');
    }
  }
};

// const handleRegister = () => {
//   console.log('Registering user:', user.value);
// };
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: linear-gradient(45deg, #240046 0%, #5a189a 100%);
  color: white;
}

.form-box {
  width: 100%;
  max-width: 500px;
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