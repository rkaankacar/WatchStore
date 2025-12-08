import React, { useState, useEffect, useMemo } from 'react';
import { Trash2, ArrowRight, ShoppingCart, Minus, Plus, Loader } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../api';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Hangi ürünün silindiğini takip etmek için
  const [deletingId, setDeletingId] = useState(null);
  // 🔥 YENİ: Hangi ürünün adedinin güncellendiğini takip etmek için
  const [updatingId, setUpdatingId] = useState(null);

  // Sayfa yüklenince sepeti çek
  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      const response = await api.get('/api/v1/cart/');
      setCartItems(response.data);
    } catch (err) {
      console.error("Sepet yüklenemedi:", err);
      setError("Sepet bilgileri alınamadı. Lütfen giriş yaptığınızdan emin olun.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (cartId) => {
    if (!window.confirm("Bu ürünü sepetten çıkarmak istiyor musun?")) return;

    setDeletingId(cartId); 

    try {
      await api.delete(`/api/v1/cart/${cartId}`);
      // Başarılı olursa listeyi güncelle
      setCartItems(prev => prev.filter(item => item.CartID !== cartId));
    } catch (err) {
      console.error("Silme hatası:", err);
      alert("Ürün silinirken bir hata oluştu.");
    } finally {
      setDeletingId(null); 
    }
  };
  
  // 🔥 YENİ: Miktar Güncelleme Fonksiyonu
  const handleQuantityChange = async (item, newQuantity) => {
    // Adet 1'den az olamaz
    if (newQuantity < 1) return;
    // Maksimum stok adedini kontrol et (API'ye göre değişebilir, burada basit bir kontrol yapıldı)
    if (item.watch && newQuantity > item.watch.Stock) {
        alert(`Maksimum stok adedi ${item.watch.Stock} olarak ayarlanabilir.`);
        return;
    }

    setUpdatingId(item.CartID); // Güncellenen öğeyi kilitle

    try {
      const payload = {
        WatchID: item.watch.WatchID, // API'nin isteyeceği WatchID
        Quantity: newQuantity
      };

      // API'ye PUT isteği gönder (Mevcut API tasarımına göre en uygun yöntem)
      await api.put(`/api/v1/cart/${item.CartID}`, payload);

      // Başarılı olursa local state'i güncelle (API'yi tekrar çekmek yerine)
      setCartItems(prev => 
        prev.map(cartItem => 
          cartItem.CartID === item.CartID ? { ...cartItem, Quantity: newQuantity } : cartItem
        )
      );
    } catch (err) {
      console.error("Miktar güncelleme hatası:", err.response?.data || err);
      alert("Miktar güncellenirken bir hata oluştu (Örn: Geçersiz miktar, stok yetersizliği).");
    } finally {
      setUpdatingId(null); // İşlem bitince kilidi aç
    }
  };

  // Toplam Tutar Hesaplama (useMemo ile performans optimizasyonu)
  const total = useMemo(() => {
    return cartItems.reduce((acc, item) => {
      const price = item.watch ? parseFloat(item.watch.Price) : 0;
      return acc + (price * item.Quantity);
    }, 0);
  }, [cartItems]);

  if (loading) return (
    <div className="d-flex justify-content-center align-items-center py-5" style={{ minHeight: '50vh' }}>
      <div className="spinner-border text-dark" role="status">
        <span className="visually-hidden">Yükleniyor...</span>
      </div>
    </div>
  );

  return (
    <div className="container py-5">
      <h2 className="fw-bold mb-4 d-flex align-items-center">
        <ShoppingCart className="me-2" size={32} />
        Alışveriş Sepeti <span className="text-muted fs-4 ms-2">({cartItems.length} Ürün)</span>
      </h2>
      
      {error && <div className="alert alert-danger">{error}</div>}

      {cartItems.length === 0 ? (
        <div className="text-center py-5 bg-light rounded-3 shadow-sm">
          <div className="mb-3 text-muted">
              <ShoppingCart size={64} opacity={0.5} />
          </div>
          <h4 className="fw-bold text-muted">Sepetin şu an bomboş! 😔</h4>
          <p className="text-muted">Hemen harika saatleri keşfetmeye başla.</p>
          <Link to="/" className="btn btn-warning fw-bold px-4 py-2 mt-2 rounded-pill shadow-sm">
            Alışverişe Başla
          </Link>
        </div>
      ) : (
        <div className="row g-4">
          {/* Ürün Listesi Sol Taraf */}
          <div className="col-lg-8">
            <div className="card border-0 shadow-sm">
              <div className="card-body p-0">
                {cartItems.map((item) => (
                  <div key={item.CartID} className="d-flex align-items-center p-3 border-bottom">
                    
                    {/* Resim Alanı */}
                    <div style={{width: '90px', height: '90px'}} className="rounded-3 bg-light border d-flex align-items-center justify-content-center p-1">
                        {item.watch && item.watch.ImageUrl ? (
                          <img 
                            src={item.watch.ImageUrl} 
                            alt={item.watch.ModelName} 
                            style={{width: '100%', height: '100%', objectFit: 'contain'}} 
                          />
                        ) : (
                          <span className="text-muted small">Resim Yok</span>
                        )}
                    </div>

                    {/* Bilgi Alanı */}
                    <div className="ms-3 flex-grow-1">
                      <h5 className="mb-1 fw-bold text-dark">
                        {item.watch ? item.watch.ModelName : "Bilinmeyen Ürün"}
                      </h5>
                      <div className="text-muted small mb-2">
                        {item.watch?.Gender} Koleksiyonu
                      </div>

                      {/* 🔥 YENİ: Adet Arttırma/Azaltma Kontrolleri */}
                      <div className="d-flex align-items-center gap-2">
                        <button
                          className="btn btn-outline-dark btn-sm p-1"
                          onClick={() => handleQuantityChange(item, item.Quantity - 1)}
                          disabled={item.Quantity <= 1 || updatingId === item.CartID}
                          title="Adeti Azalt"
                        >
                          <Minus size={16} />
                        </button>
                        
                        {updatingId === item.CartID ? (
                           <Loader size={18} className="text-dark animate-spin" />
                        ) : (
                           <span className="fw-bold px-2">{item.Quantity}</span>
                        )}

                        <button
                          className="btn btn-outline-dark btn-sm p-1"
                          onClick={() => handleQuantityChange(item, item.Quantity + 1)}
                          disabled={item.Quantity >= item.watch?.Stock || updatingId === item.CartID || !item.watch?.Stock}
                          title="Adeti Arttır"
                        >
                          <Plus size={16} />
                        </button>
                        
                        {item.watch && item.watch.Stock && (
                            <span className="text-muted small ms-2">Stok: {item.watch.Stock}</span>
                        )}
                      </div>
                      {/* Bitiş: Adet Kontrolleri */}

                    </div>

                    {/* Fiyat ve Silme Butonu */}
                    <div className="text-end">
                      <p className="mb-2 fw-bold fs-5 text-dark">
                        ₺{item.watch ? (parseFloat(item.watch.Price) * item.Quantity).toLocaleString() : 0}
                      </p>
                      <button 
                        onClick={() => handleDelete(item.CartID)}
                        className="btn btn-sm btn-outline-danger border-0 rounded-circle p-2"
                        disabled={deletingId === item.CartID} // Siliniyorsa tıklaamasın
                        title="Sepetten Çıkar"
                      >
                        {deletingId === item.CartID ? (
                           <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                        ) : (
                           <Trash2 size={18} />
                        )}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sipariş Özeti Sağ Taraf */}
          <div className="col-lg-4">
            <div className="card border-0 shadow-sm bg-white">
              <div className="card-header bg-dark text-white py-3">
                <h5 className="m-0 fw-bold">Sipariş Özeti</h5>
              </div>
              <div className="card-body p-4">
                <div className="d-flex justify-content-between mb-2">
                  <span className="text-muted">Ara Toplam</span>
                  <span className="fw-bold">₺{total.toLocaleString()}</span>
                </div>
                <div className="d-flex justify-content-between mb-3">
                  <span className="text-muted">Kargo</span>
                  <span className="text-success fw-bold">Ücretsiz</span>
                </div>
                <hr className="my-3 text-muted" />
                <div className="d-flex justify-content-between mb-4 align-items-center">
                  <span className="fw-bold fs-5">Genel Toplam</span>
                  <span className="fw-bold fs-4 text-warning">₺{total.toLocaleString()}</span>
                </div>
                
                <Link to="/checkout" className="btn btn-dark w-100 py-3 rounded-3 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2">
                  Ödemeye Geç <ArrowRight size={20} />
                </Link>
                
                <Link to="/" className="btn btn-link text-decoration-none text-muted w-100 mt-3 small">
                  &lt; Alışverişe Devam Et
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart;