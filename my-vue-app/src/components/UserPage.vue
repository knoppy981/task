<template>
  <div>
    <h1>User Page</h1>

    <div v-if="user">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
      <p><strong>Timezone:</strong> {{ user.preferences.timezone }}</p>
      <p><strong>Is Active?</strong> {{ user.isActive ? 'Yes' : 'No' }}</p>
      <p><strong>Last Updated At:</strong> {{ user.lastUpdatedAt }}</p>
      <p><strong>Created At:</strong> {{ formatTimestamp(user.created_ts) }}</p>

      <!-- Edit and Delete Actions -->
      <button @click="openEditModal">Edit</button>
      <button @click="confirmDelete">Delete</button>
    </div>

    <!-- Edit User Modal -->
    <UserModal v-if="showEditModal" :user="user" @close="showEditModal = false" @save="updateUser" />
  </div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router';
import UserModal from './UserModal.vue';
import apiService from "../../apiService"

export default {
  components: {
    UserModal
  },
  data() {
    return {
      user: null, // User object
      showEditModal: false // Edit modal visibility
    };
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    return { route, router };
  },
  methods: {
    fetchUser() {
      const userId = this.route.params.id;
      apiService.getUser(userId).then(response => {
        this.user = response.data;
      }).catch(error => {
        console.error("Error fetching user:", error);
      });
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleString();
    },
    openEditModal() {
      this.showEditModal = true;
    },

    // Call API to update an existing user
    updateUser(updatedUser) {
      console.log(updatedUser)
      apiService.editUser(updatedUser.id, updatedUser).then(() => {
        this.user = updatedUser
        this.showEditModal = false;
      }).catch(error => {
        console.error("Error updating user:", error);
      });
    },

    // Call API to delete a user
    deleteUser() {
      apiService.deleteUser(this.user.id).then(() => {
        this.$router.push('/');
      }).catch(error => {
        console.error("Error deleting user:", error);
      });
    },

    confirmDelete() {
      if (confirm(`Are you sure you want to delete ${this.user.username}?`)) {
        this.deleteUser();
      }
    },
  },
  mounted() {
    this.fetchUser(); // Fetch the user when the component is mounted
  }
};
</script>