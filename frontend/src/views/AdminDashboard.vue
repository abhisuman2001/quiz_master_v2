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
    <div class="row mt-4">
      <div class="col-12">
        <div class="summary-card p-4">
          <h4 class="text-white">Top 10 User Performance (Average Score)</h4>
          <div style="height: 400px">
            <PerformanceChart v-if="chartData.labels.length" :chart-data="chartData" />
          </div>
        </div>
      </div>
    </div>

    <hr class="text-white-50 my-4">

    <div>
      <h3 class="text-white">Global Search</h3>
      <p class="text-white-50">Search for subjects, chapters, or users across the entire platform.</p>
      <div class="mb-4">
        <input 
          type="search" 
          class="form-control form-control-lg bg-dark text-white" 
          placeholder="Start typing to search..."
          v-model="searchTerm"
        >
      </div>

      <div v-if="isLoading" class="text-center text-white-50">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      
      <div v-else-if="hasSearched">
        <p v-if="!totalResults" class="text-center text-white-50">No results found for "{{ searchTerm }}".</p>

        <div v-if="results.subjects.length" class="mb-4">
          <h4 class="text-white">Subjects</h4>
          <div class="content-card p-3">
            <ul class="list-group">
              <li v-for="item in results.subjects" :key="item.id" class="search-result-item">
                <router-link to="/admin/subjects" class="d-block text-white">
                  <strong>{{ item.name }}</strong>
                  <small class="d-block text-white-50">{{ item.description }}</small>
                </router-link>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="results.chapters.length" class="mb-4">
          <h4 class="text-white">Chapters</h4>
          <div class="content-card p-3">
            <ul class="list-group">
              <li v-for="item in results.chapters" :key="item.id" class="search-result-item">
                <router-link to="/admin/chapters" class="d-block text-white">
                  <strong>{{ item.name }}</strong>
                  <small class="d-block text-white-50">in Subject: {{ item.subject_name }}</small>
                </router-link>
              </li>
            </ul>
          </div>
        </div>

        <div v-if="results.users.length" class="mb-4">
          <h4 class="text-white">Users</h4>
          <div class="content-card p-3">
            <ul class="list-group">
              <li v-for="item in results.users" :key="item.id" class="search-result-item">
                <router-link to="/admin/users" class="d-block text-white">
                  <strong>{{ item.full_name }}</strong>
                  <small class="d-block text-white-50">{{ item.username }} ({{ item.role }})</small>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import api from '@/services/api';
import _ from 'lodash';
import PerformanceChart from '@/components/PerformanceChart.vue';

// State for Stats, Chart, and Search
const adminName = ref('');
const totalSubjects = ref(0);
const totalQuizzes = ref(0);
const totalUsers = ref(0);
const chartData = ref({ labels: [], datasets: [] });
const searchTerm = ref('');
const results = ref({ subjects: [], chapters: [], users: [] });
const isLoading = ref(false);
const hasSearched = ref(false);

// Fetch initial dashboard data (stats and chart)
onMounted(async () => {
  try {
    const [statsRes, chartRes] = await Promise.all([
      api.get('/admin/stats'),
      api.get('/admin/performance-overview')
    ]);
    
    const stats = statsRes.data;
    adminName.value = stats.admin_name;
    totalSubjects.value = stats.total_subjects;
    totalQuizzes.value = stats.total_quizzes;
    totalUsers.value = stats.total_users;

    const performanceData = chartRes.data;
    chartData.value = {
      labels: performanceData.labels,
      datasets: [ { label: 'Average Score (%)', backgroundColor: '#4361ee', data: performanceData.avg_scores } ]
    };
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  }
});

// Perform global search
const performSearch = async () => {
  if (!searchTerm.value || searchTerm.value.length < 2) {
    results.value = { subjects: [], chapters: [], users: [] };
    hasSearched.value = false;
    return;
  }
  
  isLoading.value = true;
  hasSearched.value = true;
  try {
    const response = await api.get('/admin/search', {
      params: { q: searchTerm.value }
    });
    results.value = response.data;
  } catch (error) {
    console.error("Failed to perform search:", error);
    results.value = { subjects: [], chapters: [], users: [] };
  } finally {
    isLoading.value = false;
  }
};

watch(searchTerm, _.debounce(performSearch, 500));

const totalResults = computed(() => {
  return results.value.subjects.length + results.value.chapters.length + results.value.users.length;
});
</script>

<style scoped>
.summary-card { color: white; background: rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.2); }
.content-card { background: rgba(0, 0, 0, 0.2); border-radius: 16px; }
.form-control { background-color: rgba(0,0,0,0.2); color: white; border-color: rgba(255,255,255,0.2); }
.form-control:focus { color: white; background-color: rgba(0,0,0,0.3); border-color: #ff4d6d; box-shadow: none; }
.list-group { padding: 0; }
.search-result-item { background-color: transparent; list-style: none; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
.search-result-item a { padding: 0.75rem 1.25rem; transition: background-color 0.2s ease-in-out; text-decoration: none; }
.search-result-item a:hover { background-color: rgba(255, 77, 109, 0.2); }
.search-result-item:last-child { border-bottom: none; }
</style>