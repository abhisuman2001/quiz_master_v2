<template>
  <div class="container-fluid p-4">
    <h2 class="text-white mb-4">Welcome, {{ adminName }}!</h2>
    
    <div class="row">
      <div class="col-md-4 mb-4">
        <div class="summary-card p-4">
          <h5 class="card-title">Total Subjects</h5>
          <p class="card-text display-4">{{ totalSubjects }}</p>
        </div>
      </div>
      <div class="col-md-4 mb-4">
        <div class="summary-card p-4">
          <h5 class="card-title">Total Quizzes</h5>
          <p class="card-text display-4">{{ totalQuizzes }}</p>
        </div>
      </div>
      <div class="col-md-4 mb-4">
        <div class="summary-card p-4">
          <h5 class="card-title">Registered Users</h5>
          <p class="card-text display-4">{{ totalUsers }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';

// 2. STATE VARIABLE FOR THE ADMIN'S NAME
const adminName = ref('');
const totalSubjects = ref(0);
const totalQuizzes = ref(0);
const totalUsers = ref(0);

onMounted(async () => {
  try {
    const response = await api.get('/admin/stats');
    const stats = response.data;
    
    // 3. UPDATE THE STATE WITH THE NAME FROM THE API
    adminName.value = stats.admin_name;
    totalSubjects.value = stats.total_subjects;
    totalQuizzes.value = stats.total_quizzes;
    totalUsers.value = stats.total_users;
  } catch (error) {
    console.error("Failed to fetch admin stats:", error);
    alert("Could not load dashboard statistics.");
  }
});
</script>

<style scoped>
.summary-card {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>