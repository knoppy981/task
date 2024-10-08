<template>
  <div class="modal">
    <div class="modal-content">
      <h2>{{ user ? 'Edit User' : 'Create User' }}</h2>

      <label class="modal-label" for="username">Username:</label>
      <input v-model="userData.username" type="text" id="username" />

      <label class="modal-label" for="password">Password:</label>
      <input v-model="userData.password" type="password" id="password" />

      <label for="roles">Roles:</label>
      <label for="roles">Roles:</label>
      <div>
        <div v-for="role in availableRoles" :key="role">
          <input type="checkbox" :value="role" @change="toggleRole(role)" :checked="userData.roles.includes(role)" />
          <label>{{ role }}</label>
        </div>
      </div>

      <label class="modal-label" for="timezone">Timezone:</label>
      <input v-model="userData.preferences.timezone" type="text" id="timezone" />

      <label class="modal-label" for="active">
        <input v-model="userData.active" type="checkbox" id="active" />
        Is Active?
      </label>

      <div class="modal-actions">
        <button @click="save">Save</button>
        <button @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: Object
  },
  data() {
    return {
      availableRoles: ['admin', 'manager', 'tester'],
      userData: {
        username: '',
        password: '',
        roles: [],
        preferences: { timezone: '' },
        active: false,
        ...this.user
      }
    };
  },
  methods: {
    toggleRole(role) {
      const index = this.userData.roles.indexOf(role);
      if (index > -1) {
        this.userData.roles.splice(index, 1);
      } else {
        this.userData.roles.push(role);
      }
    },
    save() {
      this.$emit('save', this.userData);
    }
  }
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
}
</style>