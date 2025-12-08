import axios from 'axios';

// Backend adresin
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

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

    // Backend'den bir cevap döndü mü?
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      // A) 401 Unauthorized (Yetkisiz Giriş / Token Süresi Bitti)
      if (status === 401) {
        // Token geçersizse temizle ve login'e at
        localStorage.removeItem('token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('user_id');

        // Eğer kullanıcı zaten login sayfasında değilse yönlendir
        if (!window.location.pathname.includes('/login')) {
          alert("Oturum süreniz doldu. Lütfen tekrar giriş yapın.");
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }

      // B) Senin errors.py yapına uygun hata yakalama
      // Backend formatı: { success: false, error: { message: "..." } }
      if (data && data.error && data.error.message) {
        errorMessage = data.error.message;

        // Eğer validasyon hatası varsa ve detayları array ise (errors.py'daki 422 yapısı)
        if (data.error.details && Array.isArray(data.error.details)) {
          errorMessage = data.error.details.join("\n"); // Hataları alt alta yaz
        }
      }
      // C) FastAPI'nin varsayılan hatası (errors.py devre dışı kalırsa)
      else if (data && data.detail) {
        errorMessage = typeof data.detail === 'string'
          ? data.detail
          : JSON.stringify(data.detail);
      }

    } else if (error.request) {
      // Sunucuya hiç ulaşılamadı (Backend kapalı veya internet yok)
      errorMessage = "Sunucuya bağlanılamadı. Lütfen internet bağlantınızı kontrol edin.";
    }

    // --- GLOBAL HATA GÖSTERİMİ ---
    // Her sayfada ayrı ayrı catch yazmak yerine burada alert veriyoruz.
    // Eğer özel bir işlem yapacaksan (örn: formu temizle), component içinde catch kullanabilirsin.

    // Sadece Login sayfasında 401 hatası için alert vermeyelim (zaten yönlendirdik)
    if (error.response?.status !== 401) {
      alert(errorMessage);
    }

    // Hatayı component'e de fırlat (belki orada loading'i kapatmak istersin)
    return Promise.reject(error);
  }
);

export default api;