import React, { useState } from 'react';
import { CreditCard, MapPin, CheckCircle, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Checkout = ({ user }) => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1); // 1: Adres, 2: Ödeme
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    fullName: user?.name || '',
    address: '',
    city: '',
    zip: '',
    cardName: '',
    cardNumber: '',
    expiry: '',
    cvv: ''
  });

  const handleOrder = (e) => {
    e.preventDefault();
    setLoading(true);

    // Sipariş işlemini simüle et (2 saniye bekle)
    setTimeout(() => {
      setLoading(false);
      alert("Siparişiniz başarıyla alındı! Teşekkür ederiz.");
      navigate('/');
    }, 2000);
  };

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
                2. Kart Bilgileri
              </span>
            </div>
          </div>

          <div className="card shadow border-0 rounded-4">
            <div className="card-body p-5">
              
              {/* ADIM 1: ADRES FORMU */}
              {step === 1 && (
                <form onSubmit={(e) => { e.preventDefault(); setStep(2); }}>
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

              {/* ADIM 2: ÖDEME FORMU */}
              {step === 2 && (
                <form onSubmit={handleOrder}>
                  <h4 className="fw-bold mb-4 d-flex align-items-center">
                    <CreditCard className="text-warning me-2" /> Ödeme Bilgileri
                  </h4>
                  
                  <div className="alert alert-light border small text-muted mb-4">
                    <CheckCircle size={14} className="text-success me-1"/> Güvenli Ödeme Altyapısı (256-bit SSL)
                  </div>

                  <div className="mb-3">
                    <label className="form-label small text-muted">Kart Üzerindeki İsim</label>
                    <input type="text" className="form-control bg-light border-0"
                      value={formData.cardName}
                      onChange={e => setFormData({...formData, cardName: e.target.value})}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Kart Numarası</label>
                    <input type="text" className="form-control bg-light border-0" placeholder="0000 0000 0000 0000"
                      value={formData.cardNumber}
                      onChange={e => setFormData({...formData, cardNumber: e.target.value})}
                      required
                    />
                  </div>
                  <div className="row g-2 mb-4">
                    <div className="col-6">
                       <label className="form-label small text-muted">Son Kullanma (AA/YY)</label>
                       <input type="text" className="form-control bg-light border-0" placeholder="MM/YY"
                         value={formData.expiry}
                         onChange={e => setFormData({...formData, expiry: e.target.value})}
                         required
                       />
                    </div>
                    <div className="col-6">
                       <label className="form-label small text-muted">CVV</label>
                       <input type="text" className="form-control bg-light border-0" placeholder="123"
                         value={formData.cvv}
                         onChange={e => setFormData({...formData, cvv: e.target.value})}
                         required
                       />
                    </div>
                  </div>

                  <div className="d-flex gap-2">
                    <button type="button" className="btn btn-light w-50 py-3 rounded-pill fw-bold text-muted" onClick={() => setStep(1)}>
                       Geri Dön
                    </button>
                    <button type="submit" className="btn btn-success w-100 py-3 rounded-pill fw-bold" disabled={loading}>
                      {loading ? 'İşleniyor...' : 'Siparişi Tamamla'}
                    </button>
                  </div>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
