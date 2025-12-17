import React, { useState, useEffect } from 'react';
import { MapPin, ArrowRight } from 'lucide-react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from "../services/api";
import { getErrorMessage } from "../utils/error";

const Checkout = ({ user }) => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [loadingPayment, setLoadingPayment] = useState(false);
  const [checkoutToken, setCheckoutToken] = useState(null);

  // State for full user data fetched from API
  const [profileUser, setProfileUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);

  const getAccessToken = () => localStorage.getItem('token');
  const userId = localStorage.getItem('user_id'); // Get ID from local storage to fetch

  useEffect(() => {
    const fetchUserProfile = async () => {
      if (!userId) {
        setLoadingUser(false);
        return;
      }
      try {
        const res = await api.get(`/api/v1/users/${userId}`);
        setProfileUser(res.data);
      } catch (err) {
        console.error("Kullanıcı bilgileri çekilemedi:", err);
      } finally {
        setLoadingUser(false);
      }
    };

    fetchUserProfile();
  }, [userId]);

  // Merge prop user (basic info) with fetched profile user (detailed info like address)
  // Priority: profileUser > user prop
  const activeUser = profileUser || user;

  // Kullanıcı bilgileri
  const fullName = activeUser?.name || activeUser?.full_name || activeUser?.FullName || '';
  const address = activeUser?.address || activeUser?.Address || '';
  const city = activeUser?.city || activeUser?.City || '';
  const zip = activeUser?.zip || '00000';
  const phone = activeUser?.phone || activeUser?.Phone || '';

  // Adres eksikse uyar
  const isAddressValid = address && city;

  const handlePayment = async () => {
    const token = getAccessToken();
    if (!token) {
      alert("Oturum bulunamadı. Lütfen giriş yapın.");
      return;
    }

    if (loadingUser) {
      return; // Wait for user data
    }

    if (!isAddressValid) {
      alert("Lütfen önce profilinizden adres bilgilerinizi güncelleyin.");
      navigate('/profil');
      return;
    }

    setLoadingPayment(true);
    try {
      const payload = {
        full_name: fullName || 'Misafir',
        address: address,
        city: city,
        zip: zip,
        gsm_number: phone || '+905555555555',
        identity_number: '11111111111'
      };

      const res = await api.post('/api/v1/payment/create', payload);
      setCheckoutToken(res.data.checkoutFormContent);
    } catch (error) {
      console.error("Ödeme başlatılamadı:", error);
      alert(getErrorMessage(error, "Ödeme başlatılamadı, tekrar deneyin."));
    } finally {
      setLoadingPayment(false);
    }
  };

  // ✅ checkoutToken geldiğinde Iyzico formunu çalıştır
  useEffect(() => {
    if (checkoutToken) {
      const container = document.getElementById('iyzipay-checkout-form');
      if (!container) return;
      container.innerHTML = checkoutToken;

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

  // Hata mesajı varsa göster
  useEffect(() => {
    const errorMsg = searchParams.get('error');
    if (errorMsg) {
      alert("Ödeme İşlemi Başarısız: " + errorMsg);
    }
  }, [searchParams]);

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="text-center mb-5">
            <h2 className="fw-bold">Ödeme ve Teslimat</h2>
          </div>

          <div className="card shadow border-0 rounded-4">
            <div className="card-body p-5">

              {!checkoutToken && (
                <>
                  <h4 className="fw-bold mb-4 d-flex align-items-center">
                    <MapPin className="text-warning me-2" /> Teslimat Adresi
                  </h4>

                  {isAddressValid ? (
                    <div className="alert alert-light border mb-4">
                      <p className="fw-bold mb-1">{fullName}</p>
                      <p className="mb-1">{address}</p>
                      <p className="mb-0 text-muted">{city} / {zip}</p>
                    </div>
                  ) : (
                    <div className="alert alert-warning mb-4">
                      Adres bilginiz eksik. Lütfen profil sayfasından guncelleyiniz.
                    </div>
                  )}

                  {isAddressValid ? (
                    <button
                      onClick={handlePayment}
                      className="btn btn-dark w-100 py-3 rounded-pill fw-bold"
                      disabled={loadingPayment}
                    >
                      {loadingPayment ? "Ödeme Başlatılıyor..." : "Ödemeye Geç"} <ArrowRight size={18} className="ms-1" />
                    </button>
                  ) : (
                    <button
                      onClick={() => navigate('/profil')}
                      className="btn btn-outline-dark w-100 py-3 rounded-pill fw-bold"
                    >
                      Adres Eklemek İçin Profile Git
                    </button>
                  )}
                </>
              )}

              <div id="iyzipay-checkout-form"></div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
