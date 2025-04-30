import axios from "axios";

const API_URL = "http://localhost:9001/api/auth";

const login = async (credentials) => {
  const { data } = await axios.post(`${API_URL}/login`, credentials);
  localStorage.setItem("token", data.token);
};

const register = async (userData) => {
  await axios.post(`${API_URL}/register`, userData);
};

const getUserData = async () => {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("No token found");

  try {
    const { data } = await axios.get(`${API_URL}/me`, {
      headers: {
        Authorization: token,
      },
    });
    return data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert("Session expired. Please log in again.");
      localStorage.removeItem("token"); // Clear token from storage
      window.location.href = "/login"; // Redirect to login page
    } else {
      throw error;
    }
  }
};

export default { login, register, getUserData };
