import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { getErrorMessage } from '../utils/error';
import api from "../services/api";

const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Her denemede hatayı temizle
    setError('');
    setLoading(true);

    try {
      // FastAPI OAuth2 "application/x-www-form-urlencoded" formatı ister
      const params = new URLSearchParams();
      params.append('username', formData.email);
      params.append('password', formData.password);

      const response = await api.post('/login', params);

      // 1. Token ve kullanıcı bilgilerini kaydet
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user_role', response.data.role);
      localStorage.setItem('user_id', response.data.user_id);
      localStorage.setItem('user_name', response.data.name);

      // 2. İsmi e-postadan türet (Geçici çözüm, backendden gelmiyorsa)
      ;

      // Ana App state'ini güncelle
      onLogin({
        name: response.data.name,
        email: formData.email,
        role: response.data.role,
        id: response.data.user_id
      });

      // 3. Anasayfaya yönlendir
      navigate('/');

    } catch (err) {
      console.error("Login Error:", err);
      setError(getErrorMessage(err, "Giriş yapılırken bir sorun oluştu."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center py-5">
      <div className="card shadow border-0" style={{ width: '400px', borderRadius: '15px' }}>
        <div className="card-body p-5">
          <h3 className="text-center fw-bold mb-4">Giriş Yap</h3>

          {/* Hata Mesajı Alanı */}
          {error && <div className="alert alert-danger text-center p-2 small">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label text-muted small">E-posta</label>
              <input
                type="email"
                className="form-control bg-light border-0"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                required
                disabled={loading} // Yüklenirken input kilitli
              />
            </div>
            <div className="mb-4">
              <label className="form-label text-muted small">Şifre</label>
              <input
                type="password"
                className="form-control bg-light border-0"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                disabled={loading} // Yüklenirken input kilitli
              />
            </div>
            <button
              className="btn btn-dark w-100 py-2 rounded-3 fw-bold shadow-sm"
              disabled={loading}
            >
              {loading ? "Giriş Yapılıyor..." : "Giriş Yap"}
            </button>
          </form>
          <div className="text-center mt-3 small">
            Hesabın yok mu? <Link to="/register" className="fw-bold text-dark text-decoration-none">Kayıt Ol</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;