<template>
  <div class="container-fluid p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="text-white">Manage Questions for Quiz #{{ quiz_id }}</h1>
      <button class="btn btn-primary" @click="openCreateModal">Create New Question</button>
    </div>

    <div v-if="!questions.length" class="content-card p-4 text-center">
      <p>No questions have been added to this quiz yet.</p>
    </div>

    <div v-for="(question, index) in questions" :key="question.id" class="content-card p-3 mb-3">
      <div class="d-flex justify-content-between">
        <p class="fw-bold">Q{{ index + 1 }}: {{ question.statement }}</p>
        <div>
          <button class="btn btn-sm btn-info me-2" @click="openEditModal(question)">Edit</button>
          <button class="btn btn-sm btn-danger" @click="deleteQuestion(question.id)">Delete</button>
        </div>
      </div>
      <div class="list-group">
        <label v-for="i in 4" :key="i" class="list-group-item" :class="{ 'correct-answer': question.correct_option === i }">
          <input class="form-check-input me-2" type="radio" :name="'q' + question.id" :checked="question.correct_option === i" disabled>
          {{ question['option' + i] }}
        </label>
      </div>
    </div>

    <div class="modal fade" id="questionModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content bg-dark text-white">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditMode ? 'Edit Question' : 'Create New Question' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateQuestion() : createQuestion()">
              <div class="mb-3">
                <label class="form-label">Question Statement</label>
                <textarea class="form-control" rows="3" v-model="currentQuestion.statement" required></textarea>
              </div>
              <p>Options (select the correct one):</p>
              <div class="row">
                <div v-for="i in 4" :key="i" class="col-md-6 mb-3">
                  <div class="input-group">
                    <div class="input-group-text">
                      <input class="form-check-input mt-0" type="radio" :value="i" v-model="currentQuestion.correct_option" name="correctOptionRadio">
                    </div>
                    <input type="text" class="form-control" :placeholder="`Option ${i}`" v-model="currentQuestion['option' + i]" required>
                  </div>
                </div>
              </div>
              <div class="modal-footer border-0">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Save Changes' : 'Create' }}</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';
import api from '../../services/api';
import { Modal } from 'bootstrap';

const props = defineProps({
  quiz_id: { type: String, required: true }
});

let questionModal = null;
const questions = ref([]);
const currentQuestion = ref({
  id: null, statement: '', option1: '', option2: '', option3: '', option4: '', correct_option: null
});
const isEditMode = ref(false);

const fetchQuestions = async () => {
  try {
    const response = await api.get(`/quizzes/${props.quiz_id}/questions`);
    questions.value = response.data;
  } catch (error) { console.error("Failed to fetch questions:", error); }
};

onMounted(() => {
  fetchQuestions();
  questionModal = new Modal(document.getElementById('questionModal'));
});

const openCreateModal = () => {
  isEditMode.value = false;
  currentQuestion.value = { id: null, statement: '', option1: '', option2: '', option3: '', option4: '', correct_option: 1 };
  questionModal.show();
};

const createQuestion = async () => {
  try {
    await api.post(`/quizzes/${props.quiz_id}/questions`, currentQuestion.value);
    questionModal.hide();
    fetchQuestions();
  } catch (error) { console.error("Failed to create question:", error); }
};

const openEditModal = (question) => {
  isEditMode.value = true;
  currentQuestion.value = { ...question };
  questionModal.show();
};

const updateQuestion = async () => {
  try {
    await api.put(`/questions/${currentQuestion.value.id}`, currentQuestion.value);
    questionModal.hide();
    fetchQuestions();
  } catch (error) { console.error("Failed to update question:", error); }
};

const deleteQuestion = async (id) => {
  if (!confirm("Are you sure you want to delete this question?")) return;
  try {
    await api.delete(`/questions/${id}`);
    fetchQuestions();
  } catch (error) { console.error("Failed to delete question:", error); }
};
</script>

<style scoped>
.content-card { background: rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(5px); }
.modal-content { background: #343a40; }
.form-control { background-color: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2); }
.form-control:focus { color: white; background-color: rgba(255,255,255,0.2); border-color: #ff4d6d; box-shadow: none; }
.list-group-item { background-color: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.2); }
.correct-answer { background-color: #198754; color: white; border-color: #198754; }
</style>