import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

let navigateFunction = null;
let logoutHandler = null;

export const setNavigator = (navigate) => { navigateFunction = navigate; };
export const setLogoutHandler = (handler) => { logoutHandler = handler; };

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status;
      if ([401,403].includes(status)) {
        localStorage.removeItem('token');
        if (logoutHandler) logoutHandler();
        if (navigateFunction) navigateFunction('/login');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
