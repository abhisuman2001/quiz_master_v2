<template>
  <div class="container-fluid p-4">
    <h1 class="text-white mb-4">Reports</h1>
    <div class="content-card p-4">
      <h4 class="text-white">User Performance Report</h4>
      <p class="text-white-50">Generate a CSV report with details of all users, including quizzes taken and average scores.</p>
      <hr class="text-white-50">

      <button class="btn btn-primary" @click="triggerReport" :disabled="isLoading">
        <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        {{ isLoading ? 'Generating...' : 'Generate User Performance CSV' }}
      </button>

      <div v-if="taskStatus" class="mt-4 alert" :class="statusClass">
        <p class="mb-1"><strong>Status:</strong> {{ taskStatus }}</p>
        <div v-if="downloadFile">
          <p class="mb-0">Your report is ready!</p>
          <a :href="downloadUrl" class="alert-link">Click here to download: {{ downloadFile }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import api from '@/services/api';

const isLoading = ref(false);
const taskId = ref(null);
const taskStatus = ref('');
const downloadFile = ref(null);
let pollingInterval = null;

const triggerReport = async () => {
  isLoading.value = true;
  taskStatus.value = 'PENDING';
  downloadFile.value = null;
  
  try {
    const response = await api.post('/admin/reports/user-performance');
    taskId.value = response.data.task_id;
    // Start polling for the status
    pollingInterval = setInterval(checkStatus, 3000);
  } catch (error) {
    console.error("Failed to trigger report:", error);
    alert('Could not start report generation.');
    isLoading.value = false;
  }
};

const checkStatus = async () => {
  try {
    const response = await api.get(`/admin/reports/status/${taskId.value}`);
    taskStatus.value = response.data.state;

    if (taskStatus.value === 'SUCCESS' || taskStatus.value === 'FAILURE') {
      isLoading.value = false;
      clearInterval(pollingInterval);
      if (taskStatus.value === 'SUCCESS') {
        downloadFile.value = response.data.result;
      }
    }
  } catch (error) {
    console.error("Failed to check status:", error);
    isLoading.value = false;
    clearInterval(pollingInterval);
  }
};

const statusClass = computed(() => {
  if (taskStatus.value === 'SUCCESS') return 'alert-success';
  if (taskStatus.value === 'FAILURE') return 'alert-danger';
  return 'alert-info';
});

const downloadUrl = computed(() => {
  // Use the full URL for the download link
  return `http://127.0.0.1:5000/api/admin/reports/download/${downloadFile.value}`;
});
</script>

<style scoped>
.content-card { background: rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(5px); }
</style>