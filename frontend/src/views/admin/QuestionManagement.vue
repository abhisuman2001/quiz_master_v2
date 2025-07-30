<template>
  <div class="container-fluid p-4">
    <h1 class="text-white mb-4">Manage Quizzes</h1>

    <div class="row mb-4">
      <div class="col-md-6">
        <label for="subjectSelect" class="form-label text-white-50">1. Select a Subject</label>
        <select class="form-select form-select-lg bg-dark text-white" id="subjectSelect" v-model="selectedSubjectId">
          <option :value="null" disabled>-- Choose a subject --</option>
          <option v-for="subject in allSubjects" :key="subject.id" :value="subject.id">
            {{ subject.name }}
          </option>
        </select>
      </div>
      <div class="col-md-6">
        <label for="chapterSelect" class="form-label text-white-50">2. Select a Chapter</label>
        <select class="form-select form-select-lg bg-dark text-white" id="chapterSelect" v-model="selectedChapterId" :disabled="!selectedSubjectId">
          <option :value="null" disabled>-- Choose a chapter --</option>
          <option v-for="chapter in chaptersForSelectedSubject" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="selectedChapterId">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="text-white">Quizzes for: {{ selectedChapterName }}</h3>
        <button class="btn btn-primary" @click="openCreateModal">Create New Quiz</button>
      </div>

      <div class="content-card p-4">
        <p v-if="!quizzes.length">No quizzes have been created for this chapter yet.</p>
        <table v-else class="table table-dark table-hover">
          <thead>
            <tr>
              <th>Quiz ID</th>
              <th>Duration (HH:MM)</th>
              <th>Remarks</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.time_duration }}</td>
              <td>{{ quiz.remarks }}</td>
              <td>
                <router-link :to="`/admin/quizzes/${quiz.id}/questions`" class="btn btn-sm btn-success me-2">
                  Manage Questions
                </router-link>
                <button class="btn btn-sm btn-info me-2" @click="openEditModal(quiz)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteQuiz(quiz.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="modal fade" id="quizModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditMode ? 'Edit Quiz' : 'Create New Quiz' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateQuiz() : createQuiz()">
              <div class="mb-3">
                <label class="form-label">Duration (HH:MM)</label>
                <input type="text" class="form-control" v-model="currentQuiz.time_duration" required placeholder="e.g., 00:30">
              </div>
              <div class="mb-3">
                <label class="form-label">Remarks</label>
                <textarea class="form-control" rows="3" v-model="currentQuiz.remarks"></textarea>
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
import { ref, onMounted, watch, computed } from 'vue';
import api from '../../services/api';
import { Modal } from 'bootstrap';

let quizModal = null;
const allSubjects = ref([]);
const chaptersForSelectedSubject = ref([]);
const quizzes = ref([]);

const selectedSubjectId = ref(null);
const selectedChapterId = ref(null);

const currentQuiz = ref({ id: null, time_duration: '', remarks: '' });
const isEditMode = ref(false);

const fetchAllSubjects = async () => {
  try {
    const response = await api.get('/subjects');
    allSubjects.value = response.data;
  } catch (error) { console.error("Failed to fetch subjects:", error); }
};

onMounted(() => {
  fetchAllSubjects();
  quizModal = new Modal(document.getElementById('quizModal'));
});

watch(selectedSubjectId, async (newSubjectId) => {
  chaptersForSelectedSubject.value = [];
  quizzes.value = [];
  selectedChapterId.value = null;
  if (newSubjectId) {
    try {
      const response = await api.get(`/subjects/${newSubjectId}/chapters`);
      chaptersForSelectedSubject.value = response.data;
    } catch (error) { console.error("Failed to fetch chapters:", error); }
  }
});

watch(selectedChapterId, async (newChapterId) => {
  quizzes.value = [];
  if (newChapterId) {
    try {
      const response = await api.get(`/chapters/${newChapterId}/quizzes`);
      quizzes.value = response.data;
    } catch (error) { console.error("Failed to fetch quizzes:", error); }
  }
});

const selectedChapterName = computed(() => {
  const chapter = chaptersForSelectedSubject.value.find(c => c.id === selectedChapterId.value);
  return chapter ? chapter.name : '';
});

const openCreateModal = () => {
  isEditMode.value = false;
  currentQuiz.value = { id: null, time_duration: '', remarks: '' };
  quizModal.show();
};

const createQuiz = async () => {
  try {
    await api.post(`/chapters/${selectedChapterId.value}/quizzes`, currentQuiz.value);
    quizModal.hide();
    const response = await api.get(`/chapters/${selectedChapterId.value}/quizzes`);
    quizzes.value = response.data;
  } catch (error) { console.error("Failed to create quiz:", error); }
};

const openEditModal = (quiz) => {
  isEditMode.value = true;
  currentQuiz.value = { ...quiz };
  quizModal.show();
};

const updateQuiz = async () => {
  try {
    await api.put(`/quizzes/${currentQuiz.value.id}`, currentQuiz.value);
    quizModal.hide();
    const response = await api.get(`/chapters/${selectedChapterId.value}/quizzes`);
    quizzes.value = response.data;
  } catch (error) { console.error("Failed to update quiz:", error); }
};

const deleteQuiz = async (id) => {
  if (!confirm("Are you sure you want to delete this quiz?")) return;
  try {
    await api.delete(`/quizzes/${id}`);
    const response = await api.get(`/chapters/${selectedChapterId.value}/quizzes`);
    quizzes.value = response.data;
  } catch (error) { console.error("Failed to delete quiz:", error); }
};
</script>

<style scoped>
.form-select { border: 1px solid rgba(255,255,255,0.2); }
.form-select:focus { box-shadow: none; border-color: #ff4d6d; }
.content-card { background: rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(5px); }
.modal-content { background: #343a40; }
.form-control { background-color: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2); }
.form-control:focus { color: white; background-color: rgba(255,255,255,0.2); border-color: #ff4d6d; box-shadow: none; }
</style>