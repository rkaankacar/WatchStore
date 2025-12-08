import axios from 'axios';

// Backend adresin
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

// Yönlendirme işlevini (navigate hook'unu) tutacak değişken
let navigateFunction = null;

// Dışarıdan navigate hook'unu alacak fonksiyon (Router'dan çağrılacak)
export const setNavigator = (navigate) => {
    navigateFunction = navigate;
};

// 1. REQUEST INTERCEPTOR (Giden İstek)
// Her istekten önce Token'ı ekler
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 2. RESPONSE INTERCEPTOR (Gelen Cevap)
// Backend'den gelen hataları merkezi olarak yakalar
api.interceptors.response.use(
  (response) => {
    // İşlem başarılıysa (200, 201 vb.) olduğu gibi devam et
    return response;
  },
  (error) => {
    let errorMessage = "Beklenmedik bir hata oluştu.";

    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      // A) 401 Unauthorized (Yetkisiz Giriş / Token Süresi Bitti)
      if (status === 401) {
        // Token geçersizse temizle
        localStorage.removeItem('token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_id');

        // React Router'ı kullanarak yönlendir
        if (navigateFunction && !window.location.pathname.includes('/login')) {
            navigateFunction('/login');
            alert("Oturum süreniz doldu. Lütfen tekrar giriş yapın.");
             // <-- React Router Yönlendirmesi
        } else if (!window.location.pathname.includes('/login')) {
             // Eğer navigate hook'u henüz yüklenmediyse, eski yöntemi kullan
             window.location.href = '/login'; 
        }
        return Promise.reject(error);
      }
      // ... (Diğer hata işleme mantığı aynı kalır) ...
      // B) Senin errors.py yapına uygun hata yakalama
      if (data && data.error && data.error.message) {
        errorMessage = data.error.message;
        if (data.error.details && Array.isArray(data.error.details)) {
          errorMessage = data.error.details.join("\n");
        }
      }
      // C) FastAPI'nin varsayılan hatası
      else if (data && data.detail) {
        errorMessage = typeof data.detail === 'string'
          ? data.detail
          : JSON.stringify(data.detail);
      }
    } else if (error.request) {
      errorMessage = "Sunucuya bağlanılamadı. Lütfen internet bağlantınızı kontrol edin.";
    }

    // --- GLOBAL HATA GÖSTERİMİ ---
    if (error.response?.status !== 401) {
      alert(errorMessage);
    }

    return Promise.reject(error);
  }
);

export default api;