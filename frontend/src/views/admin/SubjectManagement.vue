<template>
  <div class="container-fluid p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="text-white">Manage Subjects</h1>
      <button class="btn btn-primary" @click="openCreateModal">Create New Subject</button>
    </div>

    <div class="content-card p-4">
      <table class="table table-dark table-hover">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subject in subjects" :key="subject.id">
            <td>{{ subject.name }}</td>
            <td>{{ subject.description }}</td>
            <td>
              <button class="btn btn-sm btn-info me-2" @click="openEditModal(subject)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteSubject(subject.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" id="subjectModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEditMode ? 'Edit Subject' : 'Create New Subject' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateSubject() : createSubject()">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Name</label>
                <input type="text" class="form-control" id="subjectName" v-model="currentSubject.name" required>
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea class="form-control" id="subjectDescription" rows="3" v-model="currentSubject.description"></textarea>
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
import { ref, onMounted } from 'vue';
import api from '../../services/api';
import { Modal } from 'bootstrap'; // Import Bootstrap's Modal component

let subjectModal = null;

const subjects = ref([]);
const currentSubject = ref({ id: null, name: '', description: '' });
const isEditMode = ref(false);

const fetchSubjects = async () => {
  try {
    const response = await api.get('/subjects');
    subjects.value = response.data;
  } catch (error) {
    console.error("Failed to fetch subjects:", error);
    alert("Could not load subjects.");
  }
};

onMounted(() => {
  fetchSubjects();
  subjectModal = new Modal(document.getElementById('subjectModal'));
});

const openCreateModal = () => {
  isEditMode.value = false;
  currentSubject.value = { id: null, name: '', description: '' };
  subjectModal.show();
};

const createSubject = async () => {
  try {
    await api.post('/subjects', currentSubject.value);
    subjectModal.hide();
    fetchSubjects(); // Refresh list
  } catch (error) {
    console.error("Failed to create subject:", error);
    alert("Error creating subject.");
  }
};

const openEditModal = (subject) => {
  isEditMode.value = true;
  currentSubject.value = { ...subject }; // Create a copy to edit
  subjectModal.show();
};

const updateSubject = async () => {
  try {
    await api.put(`/subjects/${currentSubject.value.id}`, currentSubject.value);
    subjectModal.hide();
    fetchSubjects(); // Refresh list
  } catch (error) {
    console.error("Failed to update subject:", error);
    alert("Error updating subject.");
  }
};

const deleteSubject = async (id) => {
  if (!confirm("Are you sure you want to delete this subject?")) return;
  try {
    await api.delete(`/subjects/${id}`);
    fetchSubjects(); // Refresh list
  } catch (error) {
    console.error("Failed to delete subject:", error);
    alert("Error deleting subject.");
  }
};
</script>

<style scoped>
.content-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  backdrop-filter: blur(5px);
}
.modal-content {
  background: #343a40;
}
.form-control {
  background-color: rgba(255,255,255,0.1);
  color: white;
  border-color: rgba(255,255,255,0.2);
}
.form-control:focus {
  color: white;
  background-color: rgba(255,255,255,0.2);
  border-color: #ff4d6d;
  box-shadow: none;
}
</style>