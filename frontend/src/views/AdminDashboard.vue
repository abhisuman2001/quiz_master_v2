<template>
  <div class="container-fluid p-4">
    <h1 class="text-white mb-4">Dashboard</h1>
    
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
// This component will fetch dashboard-specific stats in the future.
// For now, we'll keep the numbers static but define them in the script.

const totalSubjects = ref(0);
const totalQuizzes = ref(0);
const totalUsers = ref(0);

// onMounted(() => {
//   // In the future, you would make API calls here to get the real numbers
//   // e.g., api.get('/admin/stats').then(res => { ... });
//   totalSubjects.value = 12;
//   totalQuizzes.value = 56;
//   totalUsers.value = 128;
// });

// For now, we'll just set them directly.
totalSubjects.value = 12;
totalQuizzes.value = 56;
totalUsers.value = 128;
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