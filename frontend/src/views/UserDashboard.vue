<template>
  <div class="dashboard-page">
    <nav class="navbar navbar-expand-lg navbar-dark top-nav">
      <div class="container-fluid">
        <a class="navbar-brand fw-bold" href="#">🚀 Quiz Master</a>
        <button @click="handleLogout" class="btn btn-outline-danger">Logout</button>
      </div>
    </nav>

    <div class="main-content container p-4">
      <h1 class="text-white mb-4">Welcome, {{ userName }}!</h1>

      <div class="row">
        <div class="col-lg-7 mb-4">
          <div class="content-card p-4">
            <h4 class="mb-3">Available Quizzes</h4>
            <p v-if="!availableQuizzes.length">No quizzes available at the moment.</p>
            <ul v-else class="list-group">
              <li v-for="quiz in availableQuizzes" :key="quiz.id" class="list-group-item d-flex justify-content-between align-items-center">
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
            <p v-if="!pastScores.length">You haven't completed any quizzes yet.</p>
            <table v-else class="table table-dark table-hover">
              <thead>
                <tr>
                  <th scope="col">Quiz</th>
                  <th scope="col">Score</th>
                  <th scope="col">Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in pastScores" :key="score.id">
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

const userName = ref('');
const availableQuizzes = ref([]);
const pastScores = ref([]);

const handleLogout = () => {
  localStorage.removeItem('accessToken');
  router.push('/login');
};

onMounted(async () => {
  try {
    const [profileRes, quizzesRes, scoresRes] = await Promise.all([
      api.get('/user/profile'),
      api.get('/quizzes'),
      api.get('/user/scores'),
    ]);

    userName.value = profileRes.data.fullName;
    availableQuizzes.value = quizzesRes.data;
    pastScores.value = scoresRes.data;

  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  }
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
  padding-top: 80px;
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
</style>