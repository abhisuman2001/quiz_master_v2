<template>
  <div class="dashboard-page">
    <div class="sidebar">
      <div class="sidebar-header">
        <h4 class="text-white">🚀 Quiz Master</h4>
        <span class="text-white-50">Admin Panel</span>
      </div>
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/admin/dashboard" class="nav-link">
            <i class="bi bi-grid-1x2-fill me-2"></i> Dashboard
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/admin/subjects" class="nav-link">
            <i class="bi bi-journal-album me-2"></i> Subjects
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
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useRouter, RouterView } from 'vue-router';

const router = useRouter();
const handleLogout = () => {
  localStorage.removeItem('accessToken');
  router.push('/login');
};
</script>

<style scoped>
/* NOTE: These styles are mostly copied from your AdminDashboard.vue */
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
  flex-shrink: 0;
}
.sidebar-header { margin-bottom: 2rem; text-align: center; }
.nav-link { color: rgba(255, 255, 255, 0.7); padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-radius: 8px; transition: all 0.3s ease; }
.nav-link:hover, .router-link-exact-active { background-color: #ff4d6d; color: white; }
.sidebar-footer { margin-top: auto; }
.main-content { flex-grow: 1; overflow-y: auto; }
</style>