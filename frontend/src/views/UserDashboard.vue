<template>
  <div class="dashboard-page">
    <nav class="navbar navbar-expand-lg navbar-dark top-nav">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">🚀 Quiz Master</a>
        <button @click="handleLogout" class="btn btn-outline-danger">Logout</button>
      </div>
    </nav>

    <div class="main-content container p-4">
      <h1 class="text-white">Welcome, {{ userName }}!</h1>
      <p class="text-white-50 mb-4">You can search for available quizzes or past scores below.</p>

      <div class="mb-4">
        <input 
          type="search" 
          class="form-control form-control-lg bg-dark text-white" 
          placeholder="Search quizzes or scores..."
          v-model="searchTerm"
        >
      </div>

      <div class="row">
        <div class="col-lg-7 mb-4">
          <div class="content-card p-4">
            <h4 class="mb-3">Available Quizzes</h4>
            <p v-if="!filteredQuizzes.length">No quizzes found matching your search.</p>
            <ul v-else class="list-group">
              <li v-for="quiz in filteredQuizzes" :key="quiz.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h6 class="mb-1">{{ quiz.title }}</h6>
                  <small class="text-muted">{{ quiz.description }}</small>
                </div>
                <router-link :to="`/quiz/${quiz.id}`" class="btn btn-primary btn-sm">Start Quiz</router-link>
              </li>
            </ul>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="content-card p-4">
            <h4 class="mb-3">My Past Scores</h4>
            <p v-if="!filteredScores.length">No scores found matching your search.</p>
            <table v-else class="table table-dark table-hover">
              <thead>
                <tr>
                  <th scope="col">Quiz</th>
                  <th scope="col">Score</th>
                  <th scope="col">Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in filteredScores" :key="score.id">
                  <td>{{ score.quizName }}</td>
                  <td>{{ score.score }}</td>
                  <td>{{ score.date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-7 mb-4">
        </div>
      <div class="col-lg-5 mb-4">
        </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="content-card p-4">
          <h4 class="mb-3">My Performance</h4>
          <div style="height: 300px">
            <PerformanceChart v-if="chartData.labels.length" :chart-data="chartData" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';
import PerformanceChart from '@/components/PerformanceChart.vue'; // Import the chart

const router = useRouter();

// State
const userName = ref('');
const availableQuizzes = ref([]);
const pastScores = ref([]);
const searchTerm = ref(''); // Single search term
const chartData = ref({ labels: [], datasets: [] }); // State for chart data

const handleLogout = () => {
  localStorage.removeItem('accessToken');
  router.push('/login');
};

// Fetch all data on component mount
onMounted(async () => {
  try {
    const [profileRes, quizzesRes, scoresRes] = await Promise.all([
      api.get('/user/profile'),
      api.get('/quizzes'), // Fetches all quizzes
      api.get('/user/scores'),
    ]);

    userName.value = profileRes.data.fullName;
    availableQuizzes.value = quizzesRes.data;
    pastScores.value = scoresRes.data;

    // Prepare data for the chart (last 5 quizzes)
    const recentScores = scoresRes.data.slice(0, 5).reverse();
    chartData.value = {
      labels: recentScores.map(s => s.quizName),
      datasets: [
        {
          label: 'Score (%)',
          backgroundColor: '#ff4d6d',
          data: recentScores.map(s => s.score)
        }
      ]
    };

  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  }
});

// --- Computed Properties for Filtering ---

// Filter available quizzes based on the single search term
const filteredQuizzes = computed(() => {
  if (!searchTerm.value) {
    return availableQuizzes.value;
  }
  const lowerCaseSearch = searchTerm.value.toLowerCase();
  return availableQuizzes.value.filter(quiz => {
    const titleMatch = quiz.title.toLowerCase().includes(lowerCaseSearch);
    const descriptionMatch = quiz.description.toLowerCase().includes(lowerCaseSearch);
    return titleMatch || descriptionMatch;
  });
});

// Filter past scores based on the single search term
const filteredScores = computed(() => {
  if (!searchTerm.value) {
    return pastScores.value;
  }
  const lowerCaseSearch = searchTerm.value.toLowerCase();
  return pastScores.value.filter(score => {
    return (
      score.quizName.toLowerCase().includes(lowerCaseSearch) ||
      score.score.toString().includes(lowerCaseSearch)
    );
  });
});
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  background: linear-gradient(45deg, #240046 0%, #5a189a 100%);
}
.top-nav {
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(5px);
}
.main-content {
  padding-top: 2rem; /* Adjusted padding */
}
.content-card {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  height: 100%;
}
.list-group-item {
  background-color: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
}
.btn-primary {
  background-color: #ff4d6d;
  border-color: #ff4d6d;
}
.form-control {
  background-color: rgba(0,0,0,0.2);
  color: white;
  border-color: rgba(255,255,255,0.2);
}
.form-control:focus {
  color: white;
  background-color: rgba(0,0,0,0.3);
  border-color: #ff4d6d;
  box-shadow: none;
}
.form-control::placeholder {
  color: rgba(255,255,255,0.4);
}
</style>