<template>
  <div class="container-fluid p-4">
    <h1 class="text-white mb-4">Manage Users</h1>

    <div class="content-card p-4">
      <table class="table table-dark table-hover">
        <thead>
          <tr>
            <th>Full Name</th>
            <th>Email</th>
            <th>Qualification</th>
            <th>Role</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.full_name }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.qualification }}</td>
            <td>{{ user.role }}</td>
            <td>
              <button class="btn btn-sm btn-info me-2" @click="openEditModal(user)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="deleteUser(user.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" id="userModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white">
          <div class="modal-header">
            <h5 class="modal-title">Edit User</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateUser">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="currentUser.full_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Email (cannot be changed)</label>
                <input type="email" class="form-control" :value="currentUser.username" disabled>
              </div>
              <div class="mb-3">
                <label class="form-label">Qualification</label>
                <input type="text" class="form-control" v-model="currentUser.qualification">
              </div>
              <div class="mb-3">
                <label class="form-label">Role</label>
                <select class="form-select bg-dark text-white" v-model="currentUser.role">
                  <option value="user">user</option>
                  <option value="admin">admin</option>
                </select>
              </div>
              <div class="modal-footer border-0">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Save Changes</button>
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
import { Modal } from 'bootstrap';

let userModal = null;
const users = ref([]);
const currentUser = ref({ id: null, full_name: '', username: '', qualification: '', role: 'user' });

const fetchUsers = async () => {
  try {
    const response = await api.get('/users');
    users.value = response.data;
  } catch (error) { console.error("Failed to fetch users:", error); }
};

onMounted(() => {
  fetchUsers();
  userModal = new Modal(document.getElementById('userModal'));
});

const openEditModal = (user) => {
  currentUser.value = { ...user };
  userModal.show();
};

const updateUser = async () => {
  try {
    await api.put(`/users/${currentUser.value.id}`, currentUser.value);
    userModal.hide();
    fetchUsers(); // Refresh list
  } catch (error) { 
    console.error("Failed to update user:", error);
    alert('Error updating user.');
  }
};

const deleteUser = async (id) => {
  if (!confirm("Are you sure you want to delete this user? This action cannot be undone.")) return;
  try {
    await api.delete(`/users/${id}`);
    fetchUsers(); // Refresh list
  } catch (error) { 
    console.error("Failed to delete user:", error); 
    alert('Error deleting user.');
  }
};
</script>

<style scoped>
/* These styles are identical to previous management pages */
.content-card { background: rgba(255, 255, 255, 0.1); border-radius: 16px; backdrop-filter: blur(5px); }
.modal-content { background: #343a40; }
.form-control, .form-select { background-color: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2); }
.form-control:focus, .form-select:focus { color: white; background-color: rgba(255,255,255,0.2); border-color: #ff4d6d; box-shadow: none; }
.form-control:disabled { background-color: rgba(0,0,0,0.4); }
</style>