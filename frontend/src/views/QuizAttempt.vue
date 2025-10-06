<template>
  <div class="quiz-page d-flex align-items-center justify-content-center">
    <div v-if="isLoading" class="text-center text-white">
      <div class="spinner-border" role="status"></div>
      <p class="mt-2">Loading Quiz...</p>
    </div>

    <div v-else-if="!isFinished" class="quiz-container card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Quiz in Progress</h5>
        <h5 class="mb-0">Time Left: <span class="badge bg-danger">{{ timeLeft }}</span></h5>
      </div>
      <div class="card-body">
        <p class="text-muted">Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</p>
        <h4 class="card-title mb-4">{{ currentQuestion.statement }}</h4>
        
        <div class="list-group">
          <label v-for="i in 4" :key="i" class="list-group-item list-group-item-action">
            <input class="form-check-input me-2" type="radio" :value="i" v-model="userAnswers[currentQuestion.id]">
            {{ currentQuestion['option' + i] }}
          </label>
        </div>
      </div>
      <div class="card-footer d-flex justify-content-between">
        <button class="btn btn-secondary" @click="prevQuestion" :disabled="currentQuestionIndex === 0">Previous</button>
        <button v-if="currentQuestionIndex < questions.length - 1" class="btn btn-primary" @click="nextQuestion">Next</button>
        <button v-else class="btn btn-success" @click="submitQuiz">Submit Quiz</button>
      </div>
    </div>

    <div v-else class="quiz-container card text-center">
      <div class="card-body">
        <h2 class="card-title">Quiz Complete!</h2>
        <p class="display-4">Your Score</p>
        <p class="display-1 fw-bold">{{ finalScore.score }} / {{ finalScore.total }}</p>
        <router-link to="/dashboard" class="btn btn-primary mt-3">Back to Dashboard</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, defineProps } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const props = defineProps({ quiz_id: { type: String, required: true } });
const router = useRouter();

const isLoading = ref(true);
const isFinished = ref(false);
const questions = ref([]);
const userAnswers = ref({});
const currentQuestionIndex = ref(0);
const timeLeft = ref('00:00');
let timerInterval = null;
const finalScore = ref({ score: 0, total: 0 });

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || {});

const fetchQuiz = async () => {
  try {
    const response = await api.get(`/quizzes/${props.quiz_id}/attempt`);
    questions.value = response.data.questions;
    startTimer(response.data.time_duration);
    isLoading.value = false;
  } catch (error) {
    console.error("Failed to load quiz:", error);
    alert('Could not load the quiz. Redirecting to dashboard.');
    router.push('/dashboard');
  }
};

const startTimer = (duration) => {
  const [hours, minutes] = duration.split(':').map(Number);
  let totalSeconds = (hours * 3600) + (minutes * 60);

  timerInterval = setInterval(() => {
    if (totalSeconds <= 0) {
      clearInterval(timerInterval);
      submitQuiz();
      return;
    }
    totalSeconds--;
    const min = Math.floor(totalSeconds / 60);
    const sec = totalSeconds % 60;
    timeLeft.value = `${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`;
  }, 1000);
};

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++;
  }
};

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
  }
};

const submitQuiz = async () => {
  clearInterval(timerInterval);
  if (!confirm("Are you sure you want to submit your quiz?")) return;
  
  try {
    const response = await api.post(`/quizzes/${props.quiz_id}/submit`, {
      answers: userAnswers.value
    });
    finalScore.value = response.data;
    isFinished.value = true;
  } catch (error) {
    console.error("Failed to submit quiz:", error);
    alert('There was an error submitting your quiz.');
  }
};

onMounted(fetchQuiz);
onUnmounted(() => {
  clearInterval(timerInterval);
});
</script>

<style scoped>
.quiz-page {
  min-height: 100vh;
  background: linear-gradient(45deg, #023e8a, #0096c7);
}
.quiz-container {
  width: 100%;
  max-width: 800px;
}
</style>