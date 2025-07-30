<template>
  <div class="container-fluid p-4">
    <h1 class="text-white mb-4">Manage Chapters</h1>

    <div class="mb-4">
      <label for="subjectSelect" class="form-label text-white-50">1. Select a Subject to Manage its Chapters</label>
      <select class="form-select form-select-lg bg-dark text-white" id="subjectSelect" v-model="selectedSubjectId">
        <option :value="null" disabled>-- Please choose a subject --</option>
        <option v-for="subject in allSubjects" :key="subject.id" :value="subject.id">
          {{ subject.name }}
        </option>
      </select>
    </div>

    <div v-if="selectedSubjectId">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="text-white">Chapters for: {{ selectedSubjectName }}</h3>
        <button class="btn btn-primary" @click="openCreateModal">Create New Chapter</button>
      </div>
      
      <div class="mb-4">
        <input 
          type="search" 
          class="form-control form-control-lg bg-dark text-white" 
          placeholder="Search for chapters in this subject..."
          v-model="chapterSearchTerm"
        >
      </div>

      <div class="content-card p-4">
        <table class="table table-dark table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th class="actions-cell">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!chapters.length">
              <td colspan="3" class="text-center">No chapters found. Try a different search.</td>
            </tr>
            <tr v-for="chapter in chapters" :key="chapter.id">
              <td>{{ chapter.name }}</td>
              <td>{{ chapter.description }}</td>
              <td class="actions-cell">
                <button class="btn btn-sm btn-info me-2" @click="openEditModal(chapter)">Edit</button>
                <button class="btn btn-sm btn-danger" @click="deleteChapter(chapter.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="modal fade" id="chapterModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditMode ? 'Edit Chapter' : 'Create New Chapter' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateChapter() : createChapter()">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input type="text" class="form-control" v-model="currentChapter.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" rows="3" v-model="currentChapter.description"></textarea>
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

let chapterModal = null;
const allSubjects = ref([]);
const selectedSubjectId = ref(null);
const chapters = ref([]);
const currentChapter = ref({ id: null, name: '', description: '' });
const isEditMode = ref(false);
const chapterSearchTerm = ref('');

const fetchAllSubjects = async () => {
  try {
    const response = await api.get('/subjects');
    allSubjects.value = response.data;
  } catch (error) {
    console.error("Failed to fetch subjects:", error);
  }
};

const fetchChaptersForSubject = async (subjectId) => {
  if (!subjectId) {
    chapters.value = [];
    return;
  }
  try {
    const response = await api.get(`/subjects/${subjectId}/chapters`, {
      params: { q: chapterSearchTerm.value }
    });
    chapters.value = response.data;
  } catch (error) {
    console.error("Failed to fetch chapters:", error);
    chapters.value = [];
  }
};

onMounted(() => {
  fetchAllSubjects();
  chapterModal = new Modal(document.getElementById('chapterModal'));
});

watch(selectedSubjectId, (newId) => {
  chapterSearchTerm.value = ''; // Reset search when subject changes
  fetchChaptersForSubject(newId);
});

watch(chapterSearchTerm, () => {
  fetchChaptersForSubject(selectedSubjectId.value);
});

const selectedSubjectName = computed(() => {
  const subject = allSubjects.value.find(s => s.id === selectedSubjectId.value);
  return subject ? subject.name : '';
});

const openCreateModal = () => {
  isEditMode.value = false;
  currentChapter.value = { id: null, name: '', description: '' };
  chapterModal.show();
};

const createChapter = async () => {
  try {
    await api.post(`/subjects/${selectedSubjectId.value}/chapters`, currentChapter.value);
    chapterModal.hide();
    fetchChaptersForSubject(selectedSubjectId.value);
  } catch (error) { console.error("Failed to create chapter:", error); }
};

const openEditModal = (chapter) => {
  isEditMode.value = true;
  currentChapter.value = { ...chapter };
  chapterModal.show();
};

const updateChapter = async () => {
  try {
    await api.put(`/chapters/${currentChapter.value.id}`, currentChapter.value);
    chapterModal.hide();
    fetchChaptersForSubject(selectedSubjectId.value);
  } catch (error) { console.error("Failed to update chapter:", error); }
};

const deleteChapter = async (id) => {
  if (!confirm("Are you sure you want to delete this chapter?")) return;
  try {
    await api.delete(`/chapters/${id}`);
    fetchChaptersForSubject(selectedSubjectId.value);
  } catch (error) { console.error("Failed to delete chapter:", error); }
};
</script>

<style scoped>
.form-select { border: 1px solid rgba(255,255,255,0.2); }
.form-select:focus { box-shadow: none; border-color: #ff4d6d; }
.actions-cell { width: 150px; text-align: right; }
.content-card { background: rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(5px); }
.modal-content { background: #343a40; }
.form-control { background-color: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2); }
.form-control:focus { color: white; background-color: rgba(255,255,255,0.2); border-color: #ff4d6d; box-shadow: none; }
</style>