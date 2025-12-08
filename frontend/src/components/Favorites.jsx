import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, ShoppingBag, Trash2, ArrowRight, AlertCircle, Loader } from 'lucide-react';
import api from '../api';

const Favorites = () => {
    const [favoriteItems, setFavoriteItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const [deletingId, setDeletingId] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchFavorites();
    }, []);

    const fetchFavorites = async () => {
        try {
            setLoading(true);
            const response = await api.get('/api/v1/favorites/');
            setFavoriteItems(response.data);
        } catch (err) {
            console.error("Favoriler yüklenirken hata:", err);
            if (err.response && err.response.status === 401) {
                navigate('/login');
            } else {
                setError("Favorileriniz yüklenirken bir sorun oluştu.");
            }
        } finally {
            setLoading(false);
        }
    };

    const handleRemoveFavorite = async (favId) => {

        if (!window.confirm("Bu ürünü favorilerden kaldırmak istediğine emin misin?")) return;

        // 🎯 FIX 1: Gelen ID'yi temiz bir tam sayıya dönüştürüyoruz.
        const numericFavId = parseInt(favId, 10);

        if (isNaN(numericFavId) || numericFavId <= 0) {
            alert("Hata: Geçersiz favori kimliği.");
            return;
        }

        setDeletingId(numericFavId);

        try {
            // DELETE isteğini gönderiyoruz
            await api.delete(`/api/v1/favorites/${numericFavId}`);

            // 🎯 CRITICAL FIX 2: Filtreleme işlemini doğru ID anahtarını bularak yapıyoruz.
            setFavoriteItems(prev => prev.filter(item => {
                // item.favoriteID veya item.favoriteid anahtarlarından hangisi varsa onu al
                const itemId = item.favoriteID || item.favoriteid;

                // Sayısal olarak karşılaştır
                return itemId !== numericFavId;
            }));

        } catch (err) {
            console.error("Silme hatası:", err);
            let errMsg = "Silinirken bir hata oluştu. Lütfen sunucu loglarını kontrol edin.";
            if (err.response && err.response.data && err.response.data.detail) {
                errMsg = err.response.data.detail;
            }
            alert(`Silme Başarısız: ${errMsg}`);

        } finally {
            setDeletingId(null);
        }
    };

    const handleAddToCart = async (watchId) => {
        try {
            await api.post('/api/v1/cart/', {
                WatchID: watchId,
                Quantity: 1
            });
            alert("Ürün başarıyla sepete eklendi! 🛒");
        } catch (err) {
            console.error("Sepet hatası:", err);
            alert("Ürün sepete eklenirken bir sorun oluştu.");
        }
    };

    if (loading) return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="spinner-border text-danger" role="status">
                <span className="visually-hidden">Yükleniyor...</span>
            </div>
        </div>
    );

    return (
        <div className="container py-5">
            {/* BAŞLIK */}
            <div className="d-flex align-items-center mb-4 border-bottom pb-3">
                <Heart className="text-danger me-2" size={32} fill="currentColor" />
                <h2 className="fw-bold m-0">Favorilerim <span className="text-muted fs-5">({favoriteItems.length})</span></h2>
            </div>

            {error && <div className="alert alert-danger rounded-3">{error}</div>}

            {favoriteItems.length === 0 ? (
                // BOŞ LİSTE GÖRÜNÜMÜ
                <div className="text-center py-5 bg-light rounded-4 shadow-sm border border-light-subtle">
                    <Heart size={64} className="text-muted opacity-25 mb-3" />
                    <h4 className="text-muted fw-bold">Listeniz henüz boş.</h4>
                    <p className="text-muted">Beğendiğiniz ürünleri kalp ikonuna tıklayarak buraya ekleyebilirsiniz.</p>
                    <Link to="/" className="btn btn-dark rounded-pill px-4 mt-2 fw-bold">
                        Keşfetmeye Başla <ArrowRight size={18} className="ms-1" />
                    </Link>
                </div>
            ) : (
                // DOLU LİSTE GÖRÜNÜMÜ
                <div className="row g-4">
                    {favoriteItems.map((item) => {
                        const product = item.watch;

                        if (!product) return null;

                        // 🎯 FIX 3: Silme ve key için kullanılacak ID'yi al
                        const favId = item.favoriteID || item.favoriteid;

                        return (
                            <div key={favId || product.WatchID} className="col-md-6 col-lg-4">
                                <div className="card h-100 border-0 shadow-sm overflow-hidden flex-row hover-shadow transition-all">

                                    {/* Sol Taraf: Resim */}
                                    <Link to={`/product/${product.WatchID}`} className="d-block bg-white border-end" style={{ width: '140px', minWidth: '140px' }}>
                                        <div className="w-100 h-100 d-flex align-items-center justify-content-center p-2 position-relative">
                                            {product.ImageUrl ? (
                                                <img
                                                    src={product.ImageUrl}
                                                    alt={product.ModelName}
                                                    style={{ maxHeight: '120px', maxWidth: '100%', objectFit: 'contain' }}
                                                />
                                            ) : (
                                                <span className="text-muted small">Resim Yok</span>
                                            )}
                                            {/* Stok Yoksa Resim Üzerine Etiket */}
                                            {product.Stock <= 0 && (
                                                <div className="position-absolute w-100 h-100 bg-white bg-opacity-75 d-flex align-items-center justify-content-center">
                                                    <span className="badge bg-secondary">Tükendi</span>
                                                </div>
                                            )}
                                        </div>
                                    </Link>

                                    {/* Sağ Taraf: Bilgiler */}
                                    <div className="card-body d-flex flex-column justify-content-between p-3">
                                        <div>
                                            <div className="d-flex justify-content-between align-items-start">
                                                <Link to={`/product/${product.WatchID}`} className="text-decoration-none text-dark">
                                                    <h6 className="card-title fw-bold mb-1 text-truncate" style={{ maxWidth: '160px' }} title={product.ModelName}>
                                                        {product.ModelName}
                                                    </h6>
                                                </Link>

                                                {/* SİLME BUTONU */}
                                                <button
                                                    onClick={() => handleRemoveFavorite(favId)}
                                                    className="btn btn-link text-danger p-0 border-0 opacity-75 hover-opacity-100"
                                                    disabled={deletingId === favId}
                                                    title="Listeden Kaldır"
                                                >
                                                    {deletingId === favId ? (
                                                        <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                                    ) : (
                                                        <Trash2 size={18} />
                                                    )}
                                                </button>
                                            </div>

                                            <div className="text-muted small mb-2">
                                                {product.BrandID ? "Lüks Seri" : "Standart"}
                                            </div>
                                            <h5 className="text-primary fw-bold mb-0">₺{parseFloat(product.Price).toLocaleString()}</h5>
                                        </div>

                                        <div className="mt-3">
                                            {product.Stock > 0 ? (
                                                <button
                                                    onClick={() => handleAddToCart(product.WatchID)}
                                                    className="btn btn-sm btn-outline-dark w-100 rounded-pill fw-bold d-flex align-items-center justify-content-center"
                                                >
                                                    <ShoppingBag size={16} className="me-1" /> Sepete Ekle
                                                </button>
                                            ) : (
                                                <button disabled className="btn btn-sm btn-light text-muted border w-100 rounded-pill">
                                                    <AlertCircle size={16} className="me-1" /> Stokta Yok
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
};

export default Favorites;