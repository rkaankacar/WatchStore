import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Watch, ShoppingBag, ArrowLeft, Star, Check, ShieldCheck, Truck, MessageSquare, Send, Heart, Trash2 } from 'lucide-react';
import api from "../services/api";
import { getErrorMessage } from "../utils/error";

const ProductDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    // --- State Tanımlamaları ---
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [adding, setAdding] = useState(false);
    const [error, setError] = useState(null);
    const [isFavorited, setIsFavorited] = useState(false);
    const [favoriteId, setFavoriteId] = useState(null);
    const [favoriting, setFavoriting] = useState(false);

    // YENİ: Carousel için index bazlı state
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    const [reviews, setReviews] = useState([]);
    const [newReview, setNewReview] = useState({ rating: 5, comment: '' });
    const [reviewSubmitting, setReviewSubmitting] = useState(false);
    const [reviewMessage, setReviewMessage] = useState('');
    const [isUserLoggedIn] = useState(!!localStorage.getItem('token'));
    const [user_id] = useState(parseInt(localStorage.getItem('user_id'))); // <-- Kullanıcı ID'sini çek
    const [deletingReviewId, setDeletingReviewId] = useState(null); // <-- Yeni State


    // --- VERİ ÇEKME FONKSİYONLARI ---
    const fetchReviews = useCallback(async () => {
        try {
            const response = await api.get(`/api/v1/reviews/?watch_id=${id}`);
            setReviews(response.data);
        } catch (err) {
            console.error("Yorumlar çekilemedi:", err);
            setReviews([]);
        }
    }, [id]);

    const checkFavoriteStatus = async () => {
        if (!isUserLoggedIn) return;
        try {
            const response = await api.get('/api/v1/favorites/');
            const existingFavorite = response.data.find(fav => fav.WatchID === parseInt(id));
            if (existingFavorite) {
                setIsFavorited(true);
                setFavoriteId(existingFavorite.FavoriteID);
            } else {
                setIsFavorited(false);
                setFavoriteId(null);
            }
        } catch (err) {
            console.error("Favori durumu kontrol edilemedi:", err);
        }
    };

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await api.get(`/api/v1/watches/${id}`);
                if (!response.data) throw new Error("Ürün verisi boş geldi.");
                setProduct(response.data);
                // Başlangıçta 0. index
                setCurrentImageIndex(0);
            } catch (err) {
                console.error("Ürün detayı alınamadı:", err);
                setError("Ürün bulunamadı veya silinmiş olabilir.");
            } finally {
                setLoading(false);
            }
        };

        fetchProduct();
        fetchReviews();
        checkFavoriteStatus();
    }, [id, fetchReviews, isUserLoggedIn]);


    // --- YENİ: 6 Saniyede Bir Otomatik Geçiş Mantığı ---
    const allImages = product
        ? [product.ImageUrl, ...(product.images || product.watch_images || []).map(i => i.ImageUrl)].filter(Boolean)
        : [];

    useEffect(() => {
        if (!allImages.length) return;

        const interval = setInterval(() => {
            setCurrentImageIndex((prevIndex) => (prevIndex + 1) % allImages.length);
        }, 6000); // 6 saniye

        return () => clearInterval(interval); // Temizlik
    }, [allImages.length]); // allImages.length değişirse (yüklenirse) timer başlasın


    // --- SEPET VE FAVORİ MANTIKLARI (Aynı kaldı) ---
    const handleAddToCart = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            // User requested no confirmation, redirect immediately or show alert
            alert("Sepete eklemek için giriş yapmalısınız.");
            navigate('/login');
            return;
        }
        setAdding(true);
        try {
            const payload = { WatchID: parseInt(id), Quantity: 1 };
            await api.post('/api/v1/cart/', payload);
            alert("Ürün başarıyla sepete eklendi! 🛒");
        } catch (err) {
            console.error("Sepet hatası:", err);
            if (err.response && err.response.status === 401) { alert("Oturum süreniz dolmuş. Lütfen tekrar giriş yapın."); navigate('/login'); }
            else { alert(getErrorMessage(err, "Ürün sepete eklenirken teknik bir sorun oluştu.")); }
        } finally {
            setAdding(false);
        }
    };

    const handleFavoriteToggle = async () => {
        if (!isUserLoggedIn) {
            // User requested no confirmation, redirect immediately or show alert
            alert("Favorilere eklemek için giriş yapmalısınız.");
            navigate('/login');
            return;
        }
        setFavoriting(true);
        setError(null);
        try {
            const watchIdInt = parseInt(id);
            if (isFavorited) {
                if (favoriteId) { await api.delete(`/api/v1/favorites/${favoriteId}`); alert("Ürün favorilerden çıkarıldı! 💔"); setIsFavorited(false); setFavoriteId(null); }
            } else {
                const payload = { watch_id: watchIdInt };
                const response = await api.post('/api/v1/favorites/', payload);
                if (response.status === 201) { alert("Ürün favorilere eklendi! ❤️"); setIsFavorited(true); setFavoriteId(response.data.FavoriteID); }
                else if (response.status === 200) { alert("Bu ürün zaten favorilerinizde."); setIsFavorited(true); setFavoriteId(response.data.FavoriteID); }
            }
        } catch (err) {
            console.error("Favori işlemi hatası:", err);
            const errMsg = getErrorMessage(err, "Favori işlemi sırasında bir hata oluştu.");
            if (errMsg.includes('already exists')) { alert("Bu ürün zaten favorilerinizde ekli."); }
            else { setError(errMsg); }
        } finally {
            setFavoriting(false);
        }
    };

    // --- YORUM SİLME FONKSİYONU ---
    const handleDeleteReview = async (reviewId) => {
        // Confirmation removed as per user request

        setDeletingReviewId(reviewId);

        try {
            // DELETE isteği: /api/v1/reviews/{reviews_id}
            await api.delete(`/api/v1/reviews/${reviewId}`);

            // Başarılı silme sonrası listeyi filtrele
            setReviews(prevReviews => prevReviews.filter(r => r.ReviewID !== reviewId));
            alert("Yorum başarıyla silindi!");

        } catch (err) {
            console.error("Yorum silme hatası:", err);
            let errMsg = getErrorMessage(err, "Yorum silinirken bir sorun oluştu.");

            if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                errMsg = "Bu yorumu silmeye yetkiniz yok (Yalnızca kendi yorumunuzu silebilirsiniz).";
            }
            alert(`Silme Başarısız: ${errMsg}`);

        } finally {
            setDeletingReviewId(null);
        }
    };


    // Yorum Gönderme Formu Değişiklik İşleyicisi (Aynı kaldı)
    const handleReviewChange = (e) => {
        const { name, value } = e.target;
        setNewReview(prev => ({
            ...prev,
            [name]: name === 'rating' ? parseInt(value) : value
        }));
    };

    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        setReviewMessage('');

        if (newReview.rating < 1 || newReview.rating > 5 || newReview.comment.length < 5) {
            setReviewMessage('Lütfen geçerli bir puan verin (1-5) ve yorumunuz en az 5 karakter olsun.');
            return;
        }

        setReviewSubmitting(true);

        try {
            const payload = {
                WatchID: parseInt(id),
                Rating: newReview.rating,
                Comment: newReview.comment
            };

            await api.post('/api/v1/reviews/', payload);
            setReviewMessage('Yorumunuz başarıyla eklendi! Sayfa yenilendiğinde göreceksiniz.');
            setNewReview({ rating: 5, comment: '' });
            fetchReviews();

        } catch (err) {
            console.error("Yorum gönderme hatası:", err);
            setReviewMessage(`Hata: ${getErrorMessage(err, "Yorum gönderilemedi.")}`);

        } finally {
            setReviewSubmitting(false);
        }
    };


    // --- RENDER KISMI ---

    if (loading) return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="spinner-border text-dark" role="status">
                <span className="visually-hidden">Yükleniyor...</span>
            </div>
        </div>
    );

    if (error || !product) {
        return (
            <div className="container py-5 text-center" style={{ minHeight: '60vh' }}>
                <div className="alert alert-warning d-inline-block px-5 py-4 rounded-3 shadow-sm">
                    <h4 className="fw-bold mb-3">Üzgünüz 😔</h4>
                    <p className="mb-4">{error}</p>
                    <Link to="/" className="btn btn-dark rounded-pill px-4">Anasayfaya Dön</Link>
                </div>
            </div>
        );
    }

    return (
        <div className="container py-5">
            {/* ... (Üst kısımlar aynı) ... */}
            <nav aria-label="breadcrumb" className="mb-4">
                <Link to="/" className="text-decoration-none text-muted d-inline-flex align-items-center hover-dark">
                    <ArrowLeft size={18} className="me-2" /> Alışverişe Dön
                </Link>
            </nav>

            <div className="row g-5">
                {/* SOL TARAF: GALERİ - YENİLENDİ CAROUSEL */}
                <div className="col-lg-6">
                    <div className="ratio ratio-1x1 rounded-4 shadow-sm d-flex align-items-center justify-content-center bg-white border mb-3 overflow-hidden position-relative">

                        {/* --- Slider Track --- */}
                        <div
                            className="d-flex w-100 h-100"
                            style={{
                                transform: `translateX(-${currentImageIndex * 100}%)`,
                                transition: 'transform 1s ease-in-out' // 1 saniye 'kayarak' geçiş
                            }}
                        >
                            {allImages.length > 0 ? (
                                allImages.map((imgSrc, index) => (
                                    <div key={index} className="flex-shrink-0 w-100 h-100 d-flex align-items-center justify-content-center p-4">
                                        <img
                                            src={imgSrc}
                                            alt={`${product.ModelName} - ${index}`}
                                            className="img-fluid"
                                            style={{ maxHeight: '100%', objectFit: 'contain' }}
                                        />
                                    </div>
                                ))
                            ) : (
                                <div className="flex-shrink-0 w-100 h-100 d-flex align-items-center justify-content-center">
                                    <Watch size={120} strokeWidth={1} className="text-muted opacity-25" />
                                </div>
                            )}
                        </div>

                        {/* Stok Rozeti */}
                        {product.Stock < 5 && product.Stock > 0 && (<span className="position-absolute top-0 end-0 m-3 badge bg-danger fs-6 shadow-sm z-3">Son {product.Stock} Ürün</span>)}
                    </div>

                    {/* Küçük Resimler (Thumbnail'ler) */}
                    <div className="d-flex gap-2 overflow-auto py-2 px-1" style={{ scrollbarWidth: 'thin' }}>
                        {allImages.map((img, index) => (
                            <div
                                key={index}
                                onClick={() => setCurrentImageIndex(index)}
                                className={`rounded-3 bg-white border d-flex align-items-center justify-content-center flex-shrink-0 cursor-pointer ${currentImageIndex === index ? 'border-warning border-2' : ''}`}
                                style={{ width: '80px', height: '80px', cursor: 'pointer', transition: 'all 0.2s' }}
                            >
                                <img src={img} alt={`Küçük Resim ${index}`} style={{ maxWidth: '90%', maxHeight: '90%', objectFit: 'contain' }} />
                            </div>
                        ))}
                    </div>
                </div>

                {/* SAĞ TARAF: BİLGİLER (Aynı kaldı) */}
                <div className="col-lg-6">
                    <div className="ps-lg-4">
                        <p className="text-dark fw-bold mb-0 text-uppercase letter-spacing-1 small">
                            {product.brand ? product.brand.BrandName : "ÖZEL KOLEKSİYON"}
                        </p>
                        <h1 className="fw-bold display-5 mb-2 text-dark">{product.ModelName}</h1>

                        <div className="d-flex align-items-center mb-4">
                            <span className="small">
                                {product.Stock > 0 ? (<span className="text-success fw-bold"><Check size={16} className="me-1" />Stokta Var ({product.Stock})</span>) : (<span className="text-danger fw-bold">Tükendi</span>)}
                            </span>
                        </div>

                        <div className="mb-4">
                            <span className="text-dark display-6 fw-bold">₺{parseFloat(product.Price).toLocaleString()}</span>
                            <span className="text-muted ms-2 small text-decoration-line-through">
                                ₺{(parseFloat(product.Price) * 1.2).toLocaleString()}
                            </span>
                        </div>

                        <p className="text-muted mb-4 lead" style={{ fontSize: '1rem', lineHeight: '1.7' }}>
                            {product.Description || "Bu ürün için henüz detaylı açıklama girilmemiş. Ancak kalitesi ve şıklığıyla sizi büyüteceğinden eminiz."}
                        </p>

                        {/* Özellikler Kutusu (Aynı kaldı) */}
                        <div className="bg-light p-4 rounded-4 mb-4 border border-light-subtle">
                            <h6 className="fw-bold mb-3 text-dark">Teknik Özellikler</h6>
                            <div className="row g-2">
                                <div className="col-6 d-flex align-items-center text-muted small"> <div className="bg-white p-2 rounded-circle me-2 shadow-sm"><Check size={14} className="text-dark" /></div> <span>Kasa: <strong>{product.CaseMaterial || "Çelik"}</strong></span> </div>
                                <div className="col-6 d-flex align-items-center text-muted small"> <div className="bg-white p-2 rounded-circle me-2 shadow-sm"><Check size={14} className="text-dark" /></div> <span>Kordon: <strong>{product.StrapMaterial || "Deri"}</strong></span> </div>
                                <div className="col-6 d-flex align-items-center text-muted small"> <div className="bg-white p-2 rounded-circle me-2 shadow-sm"><Check size={14} className="text-dark" /></div> <span>Su Geçirmezlik: <strong>{product.WaterResistance || "3 ATM"}</strong></span> </div>
                                <div className="col-6 d-flex align-items-center text-muted small"> <div className="bg-white p-2 rounded-circle me-2 shadow-sm"><Check size={14} className="text-dark" /></div> <span>Mekanizma: <strong>{product.MovementType || "Otomatik"}</strong></span> </div>
                            </div>
                        </div>

                        {/* Butonlar (Aynı kaldı) */}
                        <div className="d-flex gap-3 mb-4">
                            <button
                                onClick={handleAddToCart}
                                disabled={adding || product.Stock <= 0}
                                className={`btn btn-lg flex-grow-1 rounded-pill shadow-lg fw-bold d-flex align-items-center justify-content-center ${product.Stock <= 0 ? 'btn-secondary' : 'btn-dark'}`}
                                style={{ transition: 'transform 0.2s' }}
                            >
                                {adding ? (<> <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Ekleniyor... </>) : product.Stock <= 0 ? ("Stok Tükendi") : (<> <ShoppingBag size={22} className="me-2 mb-1" /> Sepete Ekle </>)}
                            </button>
                            <button
                                onClick={handleFavoriteToggle}
                                disabled={favoriting}
                                className="btn btn-outline-dark rounded-circle p-3"
                                title={isFavorited ? "Favorilerden Çıkar" : "Favorilere Ekle"}
                            >
                                {favoriting ? (<span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>) : isFavorited ? (<Heart size={24} fill="red" color="red" />) : (<Heart size={24} color="currentColor" />)}
                            </button>
                        </div>

                        {/* Güvenlik Rozetleri (Aynı kaldı) */}
                        <div className="d-flex gap-4 border-top pt-4">
                            <div className="d-flex align-items-center text-muted small"><Truck size={20} className="me-2 text-dark" /> Hızlı Kargo</div>
                            <div className="d-flex align-items-center text-muted small"><ShieldCheck size={20} className="me-2 text-dark" /> %100 Orijinal</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* ------------------------------------------- */}
            {/* --- YORUM ALANI --- */}
            {/* ------------------------------------------- */}
            <div className="row mt-5 pt-5 border-top">
                <div className="col-12">
                    <h3 className="fw-bold mb-4 d-flex align-items-center">
                        <MessageSquare size={28} className="me-2" /> Müşteri Yorumları ({reviews.length})
                    </h3>

                    {/* 1. Yorum Ekleme Formu (Aynı kaldı) */}
                    <div className="card shadow-sm mb-5 p-4">
                        <h5 className="fw-bold border-bottom pb-2 mb-3">Yorumunuzu Yazın</h5>

                        {/* Giriş Yapma Zorunluluğu */}
                        {!isUserLoggedIn ? (
                            <div className="alert alert-info text-center">
                                Yorum yapabilmek için lütfen <Link to="/login" className="alert-link fw-bold">Giriş Yapın</Link>.
                            </div>
                        ) : (
                            <form onSubmit={handleReviewSubmit}>

                                {reviewMessage && (
                                    <div className={`alert ${reviewMessage.includes('Hata') ? 'alert-danger' : 'alert-success'} mb-3`}>{reviewMessage}</div>
                                )}

                                {/* Puanlama (Rating) */}
                                <div className="mb-3">
                                    <label className="form-label small text-muted fw-bold">Puanınız (1-5)</label>
                                    <select
                                        name="rating"
                                        className="form-select w-auto"
                                        value={newReview.rating}
                                        onChange={handleReviewChange}
                                        required
                                    >
                                        <option value={5}>⭐⭐⭐⭐⭐ (Mükemmel)</option>
                                        <option value={4}>⭐⭐⭐⭐ (Çok İyi)</option>
                                        <option value={3}>⭐⭐⭐ (İyi)</option>
                                        <option value={2}>⭐⭐ (Fena Değil)</option>
                                        <option value={1}>⭐ (Kötü)</option>
                                    </select>
                                </div>

                                {/* Yorum Metni */}
                                <div className="mb-3">
                                    <label className="form-label small text-muted fw-bold">Yorumunuz *</label>
                                    <textarea
                                        name="comment"
                                        className="form-control"
                                        rows="3"
                                        value={newReview.comment}
                                        onChange={handleReviewChange}
                                        required
                                        minLength={5}
                                        placeholder="Ürün hakkındaki düşüncelerinizi en az 5 karakterle belirtin..."
                                    ></textarea>
                                </div>

                                <button type="submit" className="btn btn-dark rounded-pill px-4 fw-bold" disabled={reviewSubmitting}>
                                    {reviewSubmitting ? "Gönderiliyor..." : (<><Send size={18} className="me-2" /> Yorumu Gönder</>)}
                                </button>
                            </form>
                        )}
                    </div>

                    {/* 2. Yorum Listesi */}
                    <div className="mt-4">
                        {reviews.length === 0 ? (
                            <div className="alert alert-light text-center py-4">Bu ürün hakkında henüz yorum yapılmamış. İlk yorumu sen yapmak ister misin?</div>
                        ) : (
                            <div className="list-group list-group-flush">
                                {reviews.map(review => {
                                    // Puanı güvenli bir şekilde tam sayıya çevir
                                    const rawRating = review.Rating;
                                    const ratingValue = Math.round(parseFloat(rawRating));

                                    // Kullanıcı adını al
                                    const userName = review.user
                                        ? (review.user.full_name || review.user.FullName)
                                        : "Anonim Kullanıcı";

                                    // Yorumu silmek için gerekli olan ID'ler:
                                    const isAuthor = isUserLoggedIn && user_id === review.UserID;
                                    const isDeleting = deletingReviewId === review.ReviewID;

                                    return (
                                        <div key={review.ReviewID} className="list-group-item bg-white border-bottom py-4">
                                            <div className="d-flex w-100 justify-content-between">

                                                <h6 className="mb-1 fw-bold">{userName}</h6>

                                                <div className="d-flex align-items-center">
                                                    <small className="text-muted me-3">{new Date(review.CreatedAt || Date.now()).toLocaleDateString()}</small>

                                                    {/* 🚨 YORUM SİLME BUTONU 🚨 */}
                                                    {isAuthor && (
                                                        <button
                                                            onClick={() => handleDeleteReview(review.ReviewID)}
                                                            className="btn btn-link text-danger p-0 border-0"
                                                            disabled={isDeleting}
                                                            title="Yorumu Sil"
                                                        >
                                                            {isDeleting ? (
                                                                <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                                            ) : (
                                                                <Trash2 size={16} />
                                                            )}
                                                        </button>
                                                    )}
                                                </div>

                                            </div>

                                            <div className="text-warning mb-2">
                                                {/* Dolu yıldızlar */}
                                                {[...Array(ratingValue)].map((_, i) => <Star key={i} size={16} fill="currentColor" className="me-1" />)}
                                                {/* Boş yıldızlar */}
                                                {[...Array(5 - ratingValue)].map((_, i) => <Star key={i} size={16} className="text-muted me-1" />)}
                                            </div>

                                            <p className="mb-1">{review.Comment}</p>
                                        </div>
                                    );
                                })}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;