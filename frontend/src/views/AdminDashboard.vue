<template>
  <div class="dashboard-page">
    <div class="sidebar">
      <div class="sidebar-header">
        <h4 class="text-white">🚀 Quiz Master</h4>
        <span class="text-white-50">Admin Panel</span>
      </div>
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/admin/dashboard" class="nav-link active">
            <i class="bi bi-grid-1x2-fill me-2"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/subjects" class="nav-link">
            <i class="bi bi-journal-album me-2"></i> Subjects
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/quizzes" class="nav-link">
            <i class="bi bi-patch-question-fill me-2"></i> Quizzes
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/users" class="nav-link">
            <i class="bi bi-people-fill me-2"></i> Users
          </router-link>
        </li>
      </ul>
      <div class="sidebar-footer">
        <button @click="handleLogout" class="btn btn-danger w-100">
          <i class="bi bi-box-arrow-left me-2"></i> Logout
        </button>
      </div>
    </div>

    <div class="main-content">
      <div class="container-fluid p-4">
        <h1 class="text-white mb-4">Dashboard</h1>
        
        <div class="row">
          <div class="col-md-4 mb-4">
            <div class="summary-card p-4">
              <h5 class="card-title">Total Subjects</h5>
              <p class="card-text display-4">12</p>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="summary-card p-4">
              <h5 class="card-title">Total Quizzes</h5>
              <p class="card-text display-4">56</p>
            </div>
          </div>
          <div class="col-md-4 mb-4">
            <div class="summary-card p-4">
              <h5 class="card-title">Registered Users</h5>
              <p class="card-text display-4">128</p>
            </div>
          </div>
        </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
// Import Bootstrap Icons if you've installed them, or use a CDN link in your index.html
// e.g., <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">

const router = useRouter();

const handleLogout = () => {
  // 1. Remove the token from local storage
  localStorage.removeItem('accessToken');

  // 2. Redirect to the login page
  router.push('/login');
};
</script>

<style scoped>
.dashboard-page {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(45deg, #240046 0%, #5a189a 100%);
}

.sidebar {
  width: 280px;
  background: rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}
.sidebar-header {
  margin-bottom: 2rem;
  text-align: center;
}

.nav-link {
  color: rgba(255, 255, 255, 0.7);
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}
.nav-link:hover, .nav-link.active {
  background-color: #ff4d6d;
  color: white;
}

.sidebar-footer {
  margin-top: auto;
}

.main-content {
  flex-grow: 1;
  overflow-y: auto;
}

.summary-card {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>