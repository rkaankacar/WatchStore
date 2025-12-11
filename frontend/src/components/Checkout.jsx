import React, { useState, useEffect } from 'react';
import { MapPin, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Checkout = ({ user }) => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: Adres, 2: Ödeme
  const [loadingPayment, setLoadingPayment] = useState(false);
  const [formData, setFormData] = useState({
    fullName: user?.name || '',
    address: '',
    city: '',
    zip: ''
  });
  const [checkoutToken, setCheckoutToken] = useState(null);

  const getAccessToken = () => localStorage.getItem('token');

  const handlePayment = async () => {
    const token = getAccessToken();
    if (!token) {
      alert("Oturum bulunamadı. Lütfen giriş yapın.");
      setLoadingPayment(false);
      setStep(1);
      return;
    }

    setLoadingPayment(true);
    try {
      const res = await api.post('/api/v1/payment/create', {});
      setCheckoutToken(res.data.checkoutFormContent);
    } catch (error) {
      console.error("Ödeme başlatılamadı:", error.response || error);
      alert("Ödeme başlatılamadı, tekrar deneyin.");
    } finally {
      setLoadingPayment(false);
    }
  };

  const handleStep2 = (e) => {
    e.preventDefault();
    setStep(2);
    handlePayment();
  };

  // ✅ checkoutToken geldiğinde Iyzico formunu çalıştır
  useEffect(() => {
    if (checkoutToken) {
      const container = document.getElementById('iyzipay-checkout-form');
      if (!container) return;
      container.innerHTML = checkoutToken;

      // Iyzico scriptleri inline ise çalıştır
      const scripts = container.getElementsByTagName('script');
      for (let i = 0; i < scripts.length; i++) {
        const script = document.createElement('script');
        if (scripts[i].src) {
          script.src = scripts[i].src;
        } else {
          script.innerHTML = scripts[i].innerHTML;
        }
        document.body.appendChild(script);
      }
    }
  }, [checkoutToken]);

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="text-center mb-5">
            <h2 className="fw-bold">Ödeme ve Teslimat</h2>
            <div className="d-flex justify-content-center align-items-center mt-3 gap-3">
              <span className={`badge rounded-pill px-3 py-2 ${step === 1 ? 'bg-warning text-dark' : 'bg-success text-white'}`}>
                1. Adres Bilgileri
              </span>
              <ArrowRight size={16} className="text-muted" />
              <span className={`badge rounded-pill px-3 py-2 ${step === 2 ? 'bg-warning text-dark' : 'bg-secondary text-white'}`}>
                2. Ödeme
              </span>
            </div>
          </div>

          <div className="card shadow border-0 rounded-4">
            <div className="card-body p-5">

              {step === 1 && (
                <form onSubmit={handleStep2}>
                  <h4 className="fw-bold mb-4 d-flex align-items-center">
                    <MapPin className="text-warning me-2" /> Teslimat Adresi
                  </h4>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Ad Soyad</label>
                    <input type="text" className="form-control bg-light border-0" 
                      value={formData.fullName} 
                      onChange={e => setFormData({...formData, fullName: e.target.value})}
                      required 
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Adres</label>
                    <textarea className="form-control bg-light border-0" rows="2"
                      value={formData.address}
                      onChange={e => setFormData({...formData, address: e.target.value})}
                      required
                    ></textarea>
                  </div>
                  <div className="row g-2 mb-4">
                    <div className="col-8">
                      <label className="form-label small text-muted">Şehir</label>
                      <input type="text" className="form-control bg-light border-0"
                        value={formData.city}
                        onChange={e => setFormData({...formData, city: e.target.value})}
                        required
                      />
                    </div>
                    <div className="col-4">
                      <label className="form-label small text-muted">Posta Kodu</label>
                      <input type="text" className="form-control bg-light border-0"
                        value={formData.zip}
                        onChange={e => setFormData({...formData, zip: e.target.value})}
                        required
                      />
                    </div>
                  </div>
                  <button type="submit" className="btn btn-dark w-100 py-3 rounded-pill fw-bold">
                    Devam Et <ArrowRight size={18} className="ms-1" />
                  </button>
                </form>
              )}

              {step === 2 && (
                <div>
                  {loadingPayment && <p className="text-center py-5">Ödeme sayfası yükleniyor...</p>}
                  <div id="iyzipay-checkout-form"></div>
                  <button className="btn btn-light mt-3 w-100" onClick={() => setStep(1)}>Geri Dön</button>
                </div>
              )}

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
