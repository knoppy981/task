import axios from 'axios';

const API_URL = 'http://localhost:5000';  // Flask server URL

export default {
  getUsers() {
    return axios.get(`${API_URL}`);
  },

  getUser(id) {
    return axios.get(`${API_URL}/get-user/${id}`);
  },

  createUser(user) {
    return axios.post(`${API_URL}/create-user`, user, { withCredentials: true });
  },

  deleteUser(id) {
    return axios.delete(`${API_URL}/delete-user/${id}`, { withCredentials: true });
  },

  editUser(id, updatedUser) {
    return axios.post(`${API_URL}/edit-user/${id}`, updatedUser, { withCredentials: true });
  },
};