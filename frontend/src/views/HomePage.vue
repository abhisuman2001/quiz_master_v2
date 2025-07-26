<template>
  <div class="landing-page">
    <nav class="navbar navbar-expand-lg navbar-dark position-absolute w-100" style="z-index: 10; background-color: rgba(0,0,0,0.1)">
      <div class="container">
        <a class="navbar-brand fw-bold" href="#">🚀 Quiz Master</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Contact</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="hero-section d-flex align-items-center">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 text-white text-center text-lg-start">
            <h1 class="display-3 fw-bolder">Online Exam Platform</h1>
            <p class="lead my-4 text-white-50">
              The ultimate platform to test your knowledge, prepare for exams, and challenge yourself with quizzes across various subjects.
            </p>
            <div class="d-flex justify-content-center justify-content-lg-start">
              <router-link to="/login" class="btn btn-primary btn-lg me-3 px-4">Login</router-link>
              <router-link to="/register" class="btn btn-outline-light btn-lg px-4">Register</router-link>
            </div>
          </div>

          <div class="col-lg-6 d-none d-lg-flex justify-content-center">
            <svg class="illustration-svg" viewBox="0 0 569 396" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.9863 395.001H555.986" stroke="#D6D6D6" stroke-width="2" stroke-miterlimit="10"/>
                <path d="M539.99 395V1H119.99V395" stroke="#D6D6D6" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M523.49 16.9998H136.49V378.999H523.49V16.9998Z" fill="#3F3D56"/>
                <path d="M153.333 46.5H231.333M153.333 66.5H201.333" stroke="#8C8C8C" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M472.157 58.6276C477.561 58.6276 482 54.1884 482 48.7844C482 43.3804 477.561 38.9412 472.157 38.9412C466.753 38.9412 462.314 43.3804 462.314 48.7844C462.314 54.1884 466.753 58.6276 472.157 58.6276Z" fill="#6C63FF"/>
                <path d="M399.789 91.0392H185.789V346.039H399.789V91.0392Z" fill="#6C63FF"/>
                <path d="M211.725 152.922H373.843" stroke="white" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M211.725 180.314H373.843" stroke="white" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M211.725 207.706H373.843" stroke="white" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M211.725 235.098H311.235" stroke="white" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M239.118 125.529H346.333" stroke="white" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M259.412 288.608H326.039" stroke="#6C63FF" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M259.412 288.608H326.039" stroke="white" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M428.004 395V151H1V395" stroke="#D6D6D6" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M411.504 167.999H17.5039V378.999H411.504V167.999Z" fill="#3F3D56"/>
                <path d="M33.8379 197.5H111.838M33.8379 217.5H81.8379" stroke="#8C8C8C" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M148.229 288.608H214.857" stroke="#3F3D56" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M148.229 288.608H214.857" stroke="#6C63FF" stroke-width="6" stroke-miterlimit="10" stroke-linecap="round"/>
                <path d="M184.141 262.882L235.886 207.235L260.816 233.118L288.208 202.941L316.58 231.941L343.333 192.941" stroke="#FFCA28" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  /* A dark, modern purple gradient inspired by your image */
  background: linear-gradient(45deg, #240046 0%, #5a189a 100%);
  color: white;
  overflow: hidden; /* Prevents scrollbars from illustration overflow */
}

.hero-section {
  min-height: 100vh;
}

.navbar-brand {
  letter-spacing: 1px;
}

.btn-primary {
  background-color: #ff4d6d;
  border-color: #ff4d6d;
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #ff758f;
  border-color: #ff758f;
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

.btn-outline-light {
  font-weight: bold;
  padding: 0.75rem 1.5rem;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background-color: white;
  color: #240046;
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}

.illustration-svg {
  max-width: 100%;
  height: auto;
}
</style>