<template>
  <div class="main-page">
    <!-- Button for creating a new user -->
    <button @click="openCreateModal()">Create User</button>

    <!-- User Table -->
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Roles</th>
          <th>Timezone</th>
          <th>Is Active?</th>
          <th>Last Updated At</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td><router-link :to="`/user/${user.id}`">{{ user.username }}</router-link></td>
          <td>{{ user.roles }}</td>
          <td>{{ user.preferences.timezone }}</td>
          <td>{{ user.active ? 'Yes' : 'No' }}</td>
          <td>{{ user.lastUpdatedAt }}</td>
          <td>{{ formatTimestamp(user.created_ts) }}</td>
          <td>
            <button @click="openEditModal(user)">Edit</button>
            <button @click="confirmDelete(user)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Create User Modal -->
    <UserModal v-if="showCreateModal" @close="showCreateModal = false" @save="createUser" />

    <!-- Edit User Modal -->
    <UserModal v-if="showEditModal" :user="selectedUser" @close="showEditModal = false" @save="updateUser" />
  </div>
</template>

<script>
import apiService from "../../apiService"
import UserModal from './UserModal.vue';

export default {
  data() {
    return {
      users: [], // List of users
      showCreateModal: false, // Show or hide create modal
      showEditModal: false, // Show or hide edit modal
      selectedUser: null // The user selected for editing
    };
  },
  components: {
    UserModal
  },
  methods: {
    fetchUsers() {
      apiService.getUsers().then(response => {
        console.log("hi")
        console.log(response.data)
        this.users = response.data;
      }).catch(error => {
        console.error("Error fetching users:", error);
      });
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    openCreateModal() {
      this.showCreateModal = true;
    },
    openEditModal(user) {
      this.selectedUser = user;
      this.showEditModal = true;
    },

    // Call API to create a new user
    createUser(newUser) {
      apiService.createUser(newUser).then(response => {
        let newUserFromDB = response.data
        newUserFromDB.id = newUserFromDB._id
        delete newUserFromDB._id
        this.users.push(newUserFromDB);
        this.showCreateModal = false;
      }).catch(error => {
        console.error("Error creating user:", error);
      });
    },

    // Call API to update an existing user
    updateUser(updatedUser) {
      console.log(updatedUser)
      apiService.editUser(updatedUser.id, updatedUser).then(() => {
        const index = this.users.findIndex(u => u.id === updatedUser.id);
        if (index !== -1) {
          this.users.splice(index, 1, updatedUser);
        }
        this.showEditModal = false;
      }).catch(error => {
        console.error("Error updating user:", error);
      });
    },

    // Call API to delete a user
    deleteUser(user) {
      apiService.deleteUser(user.id).then(() => {
        this.users = this.users.filter(u => u.id !== user.id);
      }).catch(error => {
        console.error("Error deleting user:", error);
      });
    },

    confirmDelete(user) {
      if (confirm(`Are you sure you want to delete ${user.username}?`)) {
        this.deleteUser(user);
      }
    },
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

table,
th,
td {
  border: 1px solid black;
}

th,
td {
  padding: 10px;
  text-align: left;
}

button {
  margin: 5px;
}
</style>
