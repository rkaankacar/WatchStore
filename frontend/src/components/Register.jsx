import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api';

const Register = () => {
  // 1. State'e tüm alanları ekliyoruz
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    phone: '',
    address: '',
    city: '',
    country: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // Boş string ('') veya sadece boşlukları içeren string gelirse null döndürür.
  const getNullIfEmpty = (value) => {
    if (!value) return null;
    return value.trim() === '' ? null : value;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError('');
    setSuccess(false);
    setLoading(true);

    try {
      // 2. Payload'u temizlenmiş (null/value) değerlerle oluşturuyoruz
      const payload = {
        FullName: formData.name,
        Email: formData.email,
        Password: formData.password,
        Role: "user",
        // 👇 NULL GÖNDERME MANTIĞI BURADA 👇
        Phone: getNullIfEmpty(formData.phone),
        Address: getNullIfEmpty(formData.address),
        City: getNullIfEmpty(formData.city),
        Country: getNullIfEmpty(formData.country)
        // 👆 API'ye boşluk yerine NULL gönderir
      };

      await api.post('/api/v1/users/', payload);

      setSuccess(true);

      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (err) {
      console.error("Register Error:", err);

      let errorMessage = "Sunucu hatası oluştu. Lütfen tekrar deneyin.";

      if (err.response) {
        if (err.response.data && err.response.data.detail) {
          errorMessage = Array.isArray(err.response.data.detail)
            ? err.response.data.detail[0].msg
            : err.response.data.detail;
        }
        else if (err.response.status === 400) {
          errorMessage = "Bu e-posta adresi zaten kayıtlı.";
        } else if (err.response.status === 422) {
          errorMessage = "Girdiğiniz veriler geçersiz.";
        }
      } else {
        errorMessage = "Sunucuya bağlanılamadı.";
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center py-5">
      <div className="card shadow border-0" style={{ width: '400px', borderRadius: '15px' }}>
        <div className="card-body p-5">
          <h3 className="text-center fw-bold mb-4">Kayıt Ol</h3>

          {success ? (
            <div className="alert alert-success text-center p-2 small">
              Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz...
            </div>
          ) : error ? (
            <div className="alert alert-danger text-center p-2 small">
              {error}
            </div>
          ) : null}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label text-muted small">Ad Soyad</label>
              <input
                type="text"
                className="form-control bg-light border-0"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                disabled={loading || success}
              />
            </div>

            {/* TELEFON NUMARASI GİRİŞİ */}
            <div className="mb-3">
              <label className="form-label text-muted small">Telefon Numarası (Opsiyonel)</label>
              <input
                type="text"
                className="form-control bg-light border-0"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                disabled={loading || success}
              />
            </div>

            {/* E-POSTA GİRİŞİ */}
            <div className="mb-3">
              <label className="form-label text-muted small">E-posta</label>
              <input
                type="email"
                className="form-control bg-light border-0"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                disabled={loading || success}
              />
            </div>

            {/* ŞİFRE GİRİŞİ */}
            <div className="mb-4">
              <label className="form-label text-muted small">Şifre</label>
              <input
                type="password"
                className="form-control bg-light border-0"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                disabled={loading || success}
              />
            </div>

            <button
              className="btn btn-warning w-100 py-2 rounded-3 fw-bold shadow-sm"
              disabled={loading || success}
            >
              {loading ? "Kaydediliyor..." : "Kayıt Ol"}
            </button>
          </form>

          <div className="text-center mt-3 small">
            Zaten hesabın var mı? <Link to="/login" className="fw-bold text-dark text-decoration-none">Giriş Yap</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;