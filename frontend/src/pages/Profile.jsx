import React, { useState, useEffect } from "react";
import { ShoppingBag, User, MapPin, KeyRound, RefreshCw, Loader, ArrowLeft, Send } from "lucide-react";
import { useNavigate, useSearchParams } from "react-router-dom";
import api from "../services/api";
import { getErrorMessage } from "../utils/error";

// ==========================================================
// YARDIMCI FONKSİYON: Sipariş Durumu Etiketi (Badge)
// ==========================================================
const getStatusBadge = (status) => {
    switch (status) {
        case 'Teslim Edildi':
            return <span className="badge bg-success">Teslim Edildi</span>;
        case 'Kargoda':
            return <span className="badge bg-primary">Kargoda</span>;
        case 'İptal Edildi':
            return <span className="badge bg-danger">İptal Edildi</span>;
        case 'Hazırlanıyor':
        default:
            return <span className="badge bg-warning text-dark">Hazırlanıyor</span>;
    }
};

// ==========================================================
// YARDIMCI BİLEŞEN: İade/Değişim Talep Formu
// ==========================================================
const ReturnRequestForm = ({ order, onBack, onSubmit, isSubmitting }) => {

    // Form State'leri
    const [requestData, setRequestData] = useState({
        RequestType: 'İade', // Varsayılan: İade
        Reason: '',
        Description: ''
    });

    // SEÇİLEN ÜRÜNLER STATE'İ
    // Başlangıçta hepsi seçili olsun mu? Veya hiçbiri? Kullanıcı deneyimi için boş bırakalım.
    const [selectedDetailIds, setSelectedDetailIds] = useState([]);

    const handleFormChange = (e) => {
        setRequestData(prev => ({
            ...prev,
            [e.target.name]: e.target.value
        }));
    };

    // Checkbox değişimi
    const handleProductToggle = (detailId) => {
        setSelectedDetailIds(prev => {
            if (prev.includes(detailId)) {
                return prev.filter(id => id !== detailId);
            } else {
                return [...prev, detailId];
            }
        });
    };

    // "Tümünü Seç" fonksiyonu (Opsiyonel ama şık olur)
    const handleSelectAll = () => {
        if (selectedDetailIds.length === order.order_details.length) {
            setSelectedDetailIds([]);
        } else {
            setSelectedDetailIds(order.order_details.map(d => d.OrderDetailID));
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (selectedDetailIds.length === 0) {
            alert("Lütfen iade/değişim yapılacak en az bir ürün seçiniz.");
            return;
        }

        if (!requestData.Reason) {
            alert("Lütfen talep nedenini belirtiniz.");
            return;
        }

        // Ana Profile bileşenine HEM verileri HEM DE seçilen ID'leri gönderiyoruz
        onSubmit(order.OrderID, requestData, selectedDetailIds);
    };

    return (
        <div className="card p-4 shadow-sm border-0">
            <div className="d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
                <h4 className="fw-bold m-0">
                    Talep Oluştur: Sipariş #{order.OrderID}
                </h4>
                <button className="btn btn-sm btn-outline-dark" onClick={onBack} disabled={isSubmitting}>
                    <ArrowLeft size={16} className="me-1" /> Sipariş Detayına Dön
                </button>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="row g-3">

                    {/* --- ÜRÜN SEÇİM ALANI --- */}
                    <div className="col-12 mb-3">
                        <div className="d-flex justify-content-between align-items-center mb-2">
                            <label className="form-label fw-bold m-0">İade Edilecek Ürünleri Seçiniz *</label>
                            <button
                                type="button"
                                className="btn btn-link btn-sm text-decoration-none p-0"
                                onClick={handleSelectAll}
                            >
                                {selectedDetailIds.length === order.order_details.length ? "Seçimi Kaldır" : "Tümünü Seç"}
                            </button>
                        </div>

                        <div className="list-group">
                            {order.order_details.map(item => (
                                <label key={item.OrderDetailID} className="list-group-item d-flex align-items-center" style={{ cursor: 'pointer' }}>
                                    <input
                                        className="form-check-input me-3"
                                        type="checkbox"
                                        checked={selectedDetailIds.includes(item.OrderDetailID)}
                                        onChange={() => handleProductToggle(item.OrderDetailID)}
                                    />
                                    <img
                                        src={item.watch?.ImageUrl || "https://via.placeholder.com/40"}
                                        alt="Ürün"
                                        style={{ width: '40px', height: '40px', objectFit: 'contain' }}
                                        className="me-3 rounded border"
                                    />
                                    <div className="flex-grow-1">
                                        <div className="fw-bold">{item.watch?.ModelName || 'Ürün Adı Yok'}</div>
                                        <div className="small text-muted">Adet: {item.Quantity}</div>
                                    </div>
                                    <div className="fw-bold">₺{parseFloat(item.UnitPrice).toLocaleString()}</div>
                                </label>
                            ))}
                        </div>
                        <div className="form-text mt-1">
                            Seçilen ürünler: {selectedDetailIds.length} adet
                        </div>
                    </div>


                    <div className="col-md-6 mb-3">
                        <label className="form-label fw-bold">Talep Tipi *</label>
                        <select
                            name="RequestType"
                            value={requestData.RequestType}
                            onChange={handleFormChange}
                            className="form-select bg-light border-0"
                            required
                        >
                            <option value="İade">İade (Geri Ödeme)</option>
                            <option value="Değişim">Değişim (Başka Ürün/Boyut)</option>
                        </select>
                    </div>

                    <div className="col-md-6 mb-3">
                        <label className="form-label fw-bold">Neden *</label>
                        <select
                            name="Reason"
                            value={requestData.Reason}
                            onChange={handleFormChange}
                            className="form-select bg-light border-0"
                            required
                        >
                            <option value="">Seçiniz</option>
                            <option value="Ürün Kusurlu/Hasarlı">Ürün Kusurlu/Hasarlı</option>
                            <option value="Beden/Boyut Uymadı">Beden/Boyut Uymadı</option>
                            <option value="Yanlış Ürün Gönderildi">Yanlış Ürün Gönderildi</option>
                            <option value="Beklentimi Karşılamadı">Beklentimi Karşılamadı</option>
                            <option value="Vazgeçtim">Fikrimi Değiştirdim / Vazgeçtim</option>
                            <option value="Diğer">Diğer (Açıklama Gerekli)</option>
                        </select>
                    </div>

                    <div className="col-12 mb-4">
                        <label className="form-label fw-bold">Açıklama (Opsiyonel)</label>
                        <textarea
                            name="Description"
                            value={requestData.Description}
                            onChange={handleFormChange}
                            className="form-control bg-light border-0"
                            rows="4"
                            placeholder="Talebinizle ilgili detaylı bilgi ve beklentinizi yazınız."
                        ></textarea>
                    </div>

                    <div className="col-12 text-end">
                        <button type="submit" className="btn btn-dark px-4" disabled={isSubmitting}>
                            <Send size={18} className="me-2 mb-1" />
                            {isSubmitting ? "Gönderiliyor..." : "Talebi Gönder"}
                        </button>
                    </div>
                </div>
            </form>
        </div>
    );
};


// ==========================================================
// YARDIMCI BİLEŞEN: Sipariş Detay Sayfası
// ==========================================================
const OrderDetail = ({ orderId, onBack, onCancel, onRequestReturn, isSubmitting, getStatusBadge, orderDetail }) => {

    // Yükleme sırasında geçici olarak null olabilir
    if (!orderDetail) {
        return (
            <div className="text-center py-5">
                <Loader size={32} className="spinner-border text-dark" />
                <p className="mt-3 text-muted">Sipariş detayı yükleniyor...</p>
            </div>
        );
    }
    const detail = orderDetail;

    return (
        <div className="card p-4 shadow-sm border-0">
            <div className="d-flex justify-content-between align-items-start mb-4 border-bottom pb-2">
                <h4 className="fw-bold m-0">
                    Sipariş Detayı: #{detail.OrderID}
                </h4>

                <div className="d-flex align-items-center">
                    {/* İptal Butonu (Hazırlanıyor iken) */}
                    {detail.Status === 'Hazırlanıyor' && (
                        <button
                            className="btn btn-sm btn-danger me-3"
                            onClick={() => onCancel(detail.OrderID)}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'İptal Ediliyor...' : 'Siparişi İptal Et'}
                        </button>
                    )}

                    {/* İade/Değişim Butonu (Tamamlandı/Teslim Edildi ise) */}
                    {detail.Status === 'Teslim Edildi' && (
                        <button
                            className="btn btn-sm btn-outline-warning me-3"
                            onClick={() => onRequestReturn(detail)} // Formu açacak fonksiyon
                            disabled={isSubmitting}
                        >
                            İade/Değişim Talebi
                        </button>
                    )}

                    <button className="btn btn-sm btn-outline-dark" onClick={onBack} disabled={isSubmitting}>
                        <ArrowLeft size={16} className="me-1" /> Listeye Dön
                    </button>
                </div>

            </div>

            <div className="row mb-4">
                <div className="col-md-4">
                    <p className="small text-muted mb-1">Durum</p>
                    <p className="fw-bold">{getStatusBadge(detail.Status)}</p>
                </div>
                <div className="col-md-4">
                    <p className="small text-muted mb-1">Sipariş Tarihi</p>
                    <p className="fw-bold">{new Date(detail.OrderDate).toLocaleDateString('tr-TR')}</p>
                </div>
                <div className="col-md-4">
                    <p className="small text-muted mb-1">Toplam Tutar</p>
                    <p className="fw-bold text-success">₺{parseFloat(detail.TotalAmount).toLocaleString()}</p>
                </div>
            </div>

            <h5 className="fw-bold mb-3 border-bottom pb-1">Teslimat Adresi</h5>
            <p>{detail.ShippingAddress || "Adres bilgisi mevcut değil."}</p>

            <h5 className="fw-bold mt-4 mb-3 border-bottom pb-1">Ürünler ({detail.order_details.length})</h5>

            <ul className="list-group list-group-flush">
                {detail.order_details.map(item => (
                    <li key={item.OrderDetailID} className="list-group-item d-flex justify-content-between align-items-center">
                        <div className="d-flex align-items-center">
                            <img
                                src={item.watch?.ImageUrl || "https://via.placeholder.com/40"}
                                alt="Ürün"
                                style={{ width: '40px', height: '40px', objectFit: 'contain' }}
                                className="me-3 rounded border"
                            />
                            <div>
                                <span className="fw-bold">{item.watch?.ModelName || 'Ürün Adı Yok'}</span>
                                <span className="text-muted d-block small">Marka: {item.watch?.brand?.BrandName || 'Bilinmiyor'}</span>
                            </div>
                        </div>
                        <span className="text-end">
                            <span className="d-block fw-bold text-dark">{item.Quantity} x ₺{parseFloat(item.UnitPrice).toLocaleString()}</span>
                            <span className="small text-muted">Ara Toplam: ₺{(item.Quantity * parseFloat(item.UnitPrice)).toLocaleString()}</span>
                        </span>
                    </li>
                ))}
            </ul>

        </div>
    );
};


// ==========================================================
// ANA BİLEŞEN: Profile.js
// ==========================================================
const Profile = ({ user }) => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    const [activeTab, setActiveTab] = useState("orders");
    const [selectedOrderId, setSelectedOrderId] = useState(null);
    const [orderToReturn, setOrderToReturn] = useState(null); // İade/Değişim formu için state

    const [userData, setUserData] = useState({ Email: "", Phone: "", Address: "", City: "", Country: "" });
    const [passwordData, setPasswordData] = useState({ currentPassword: "", newPassword: "", confirmNewPassword: "" });
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [ordersLoading, setOrdersLoading] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState("");
    const [isError, setIsError] = useState(false);
    const [currentOrderDetail, setCurrentOrderDetail] = useState(null); // Detay verisini tutar

    const USER_ID = user?.UserID || user?.id;

    const ENDPOINTS = {
        USER_INFO: `/api/v1/users/${USER_ID}`,
        USER_UPDATE: `/api/v1/users/update/${USER_ID}`,
        PASSWORD_CHANGE: `/api/v1/users/change-password`,
        USER_ORDERS: `/api/v1/orders/`,
        CREATE_RETURN: `/api/v1/returns/`
    };

    // --- VERİ ÇEKME FONKSİYONLARI ---

    const fetchUserData = async () => {
        setLoading(true);
        setIsError(false);
        setMessage("");
        try {
            const userRes = await api.get(ENDPOINTS.USER_INFO);
            setUserData({
                Email: userRes.data.email || userRes.data.Email || "",
                Phone: userRes.data.phone || userRes.data.Phone || "",
                Address: userRes.data.address || userRes.data.Address || "",
                City: userRes.data.city || userRes.data.City || "",
                Country: userRes.data.country || userRes.data.Country || "",
            });
        } catch (err) {
            console.error("Kullanıcı bilgisi çekilemedi:", err);
            setIsError(true);
            setMessage(getErrorMessage(err, "Kullanıcı bilgileri yüklenemedi."));
        } finally {
            setLoading(false);
        }
    };

    const fetchOrders = async () => {
        setOrdersLoading(true);
        try {
            const orderRes = await api.get(ENDPOINTS.USER_ORDERS);
            const sortedOrders = (orderRes.data || []).sort((a, b) => b.OrderID - a.OrderID);
            setOrders(sortedOrders);
        } catch (err) {
            console.error("Siparişler çekilemedi:", err);
            if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                setMessage(getErrorMessage(err, "Siparişleri görüntüleme yetkiniz yok veya oturumunuz sona erdi."));
                setIsError(true);
            }
            setOrders([]);
        } finally {
            setOrdersLoading(false);
        }
    };

    const fetchOrderDetail = async (orderId) => {
        try {
            setOrdersLoading(true);
            const res = await api.get(`/api/v1/orders/${orderId}`);
            setCurrentOrderDetail(res.data);
            return res.data;
        } catch (err) {
            console.error("Detay çekilemedi:", err);
            setCurrentOrderDetail(null);
            return null;
        } finally {
            setOrdersLoading(false);
        }
    }

    const fetchData = async () => {
        await fetchUserData();
        if (activeTab === "orders") {
            setSelectedOrderId(null);
            setOrderToReturn(null);
            await fetchOrders();
        }
    };

    // --- LIFE CYCLE VE LOGIC ---

    useEffect(() => {
        if (!USER_ID) {
            setLoading(false);
            setIsError(true);
            setMessage("Kullanıcı ID bulunamadı.");
            return;
        }
        fetchUserData();
    }, [USER_ID]);

    useEffect(() => {
        if (activeTab === "orders" && USER_ID && (orders.length === 0 || !ordersLoading)) {
            fetchOrders();
        }
        if (activeTab !== "orders" && (selectedOrderId !== null || orderToReturn !== null)) {
            setSelectedOrderId(null);
            setOrderToReturn(null);
        }
    }, [activeTab, USER_ID]);

    // YENİ: URL'den order_id geldiğinde o siparişi aç
    useEffect(() => {
        const orderIdParam = searchParams.get('order_id');
        if (orderIdParam) {
            const orderId = parseInt(orderIdParam);
            if (!isNaN(orderId)) {
                setActiveTab("orders"); // Emin olalım
                setSelectedOrderId(orderId);
                fetchOrderDetail(orderId);
            }
        }
    }, [searchParams]);


    // --- SİPARİŞ İŞLEMLERİ ---

    // YENİ: Talep Formunu Gösterme
    const handleRequestReturn = (order) => {
        setOrderToReturn(order); // İade edilecek siparişi kaydet
        setSelectedOrderId(order.OrderID); // Detay sayfasını açık tut (gerekirse)
    };

    // YENİ: Formdan Gelen Talebi Gönderme
    const handleReturnSubmit = async (orderId, data, selectedDetailIds) => {
        setSubmitting(true);
        setMessage("");

        // Hata ve Başarı sayaçları
        let successCount = 0;
        let failCount = 0;

        try {
            // Seçilen her bir ürün için ayrı istek atıyoruz
            const promises = selectedDetailIds.map(detailId => {
                const payload = {
                    OrderID: orderId,
                    OrderDetailID: detailId, // Burası ARTIK ekleniyor
                    RequestType: data.RequestType,
                    Reason: data.Reason,
                    Description: data.Description,
                };
                return api.post(ENDPOINTS.CREATE_RETURN, payload)
                    .then(() => { successCount++; })
                    .catch((e) => {
                        console.error(`ID ${detailId} için hata:`, e);
                        failCount++;
                    });
            });

            // Tüm isteklerin bitmesini bekle
            await Promise.all(promises);

            if (successCount > 0) {
                let msg = `${successCount} adet ürün için talep başarıyla oluşturuldu.`;
                if (failCount > 0) {
                    msg += ` (${failCount} ürün başarısız oldu)`;
                    setIsError(true); // Kısmi hata
                } else {
                    setIsError(false);
                }
                setMessage(msg);

                // Başarılı işlem varsa listeye dön
                setOrderToReturn(null);
                handleBackToOrders();
            } else {
                setMessage("Talepler oluşturulurken bir hata oluştu.");
                setIsError(true);
            }

        } catch (err) {
            console.error("Genel talep gönderme hatası:", err);
            setIsError(true);
            setMessage(getErrorMessage(err, "Talep işlemleri sırasında beklenmedik hata oluştu."));
        } finally {
            setSubmitting(false);
        }
    };

    const handleCancelOrder = async (orderId) => {
        // Confirmation removed as per user request

        setSubmitting(true);
        setMessage("");

        try {
            const payload = { "Status": "İptal Edildi" };
            const response = await api.patch(`/api/v1/orders/${orderId}/status`, payload);
            const cancelledOrder = response.data;

            setOrders(prevOrders => prevOrders.map(order =>
                order.OrderID === orderId ? cancelledOrder : order
            ).sort((a, b) => b.OrderID - a.OrderID));

            setSelectedOrderId(cancelledOrder.OrderID);
            setCurrentOrderDetail(cancelledOrder); // Detay bileşenini anında güncelle

            setMessage(`Sipariş #${orderId} başarıyla iptal edildi.`);
            setIsError(false);

        } catch (err) {
            console.error("İptal hatası:", err);
            setIsError(true);
            setMessage(getErrorMessage(err, "Sipariş iptal edilirken bir hata oluştu."));
        } finally {
            setSubmitting(false);
        }
    };

    const handleOrderClick = (id) => {
        setSelectedOrderId(id);
        fetchOrderDetail(id);
        setOrderToReturn(null);
    };

    const handleBackToOrders = () => {
        setSelectedOrderId(null);
        setOrderToReturn(null);
        fetchOrders();
    };


    // --- BİLGİ/ŞİFRE GÜNCELLEME ---

    const handleInfoChange = (e) => { setUserData((prev) => ({ ...prev, [e.target.name]: e.target.value })); };
    const handlePasswordChange = (e) => { setPasswordData((prev) => ({ ...prev, [e.target.name]: e.target.value })); };

    const handleInfoSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setMessage("");
        try { await api.put(ENDPOINTS.USER_UPDATE, userData); setMessage("Bilgiler başarıyla güncellendi!"); setIsError(false); }
        catch (err) { console.error("Güncelleme hatası:", err); setIsError(true); setMessage(getErrorMessage(err, "Bilgiler güncellenirken hata oluştu.")); }
        finally { setSubmitting(false); }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();
        if (passwordData.newPassword !== passwordData.confirmNewPassword) { setIsError(true); setMessage("Yeni şifreler uyuşmuyor."); return; }
        if (passwordData.newPassword.length < 6) { setIsError(true); setMessage("Yeni şifre en az 6 karakter olmalı."); return; }
        setSubmitting(true);
        setMessage("");
        try {
            await api.put(ENDPOINTS.PASSWORD_CHANGE, { current_password: passwordData.currentPassword, new_password: passwordData.newPassword, new_password_again: passwordData.confirmNewPassword });
            setMessage("Şifre başarıyla değiştirildi!"); setIsError(false); setPasswordData({ currentPassword: "", newPassword: "", confirmNewPassword: "" });
        } catch (err) {
            console.error("Şifre değiştirme hatası:", err); setIsError(true); setMessage(getErrorMessage(err, "Şifre güncellenemedi."));
        } finally { setSubmitting(false); }
    };


    if (loading) return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <Loader size={32} className="spinner-grow text-dark" />
        </div>
    );

    return (
        <div className="container py-5">
            {/* ... Başlık ve Yenile Butonu ... */}
            <div className="d-flex align-items-center justify-content-between mb-4">
                <div className="d-flex align-items-center text-dark">
                    <User size={32} className="me-2" />
                    <h2 className="fw-bold m-0 text-dark">Profilim</h2>
                </div>
                <button className="btn btn-outline-dark btn-sm rounded-pill px-3" onClick={fetchData} disabled={submitting}>
                    <RefreshCw size={16} className="me-1" /> Yenile
                </button>
            </div>

            <div className="row">
                <div className="col-md-3 mb-4">
                    <div className="list-group shadow-sm border-0">
                        {/* ... Sekmeler ... */}
                        <button
                            className={`list-group-item list-group-item-action py-3 ${activeTab === "orders" ? "active bg-dark text-white fw-bold" : ""
                                }`}
                            onClick={() => { setActiveTab("orders"); setSelectedOrderId(null); setOrderToReturn(null); }}
                        >
                            <ShoppingBag size={18} className="me-2" /> Siparişlerim
                        </button>
                        <button
                            className={`list-group-item list-group-item-action py-3 ${activeTab === "info" ? "active bg-dark text-white fw-bold" : ""
                                }`}
                            onClick={() => setActiveTab("info")}
                        >
                            <User size={18} className="me-2" /> Bilgilerim
                        </button>
                    </div>
                </div>

                <div className="col-md-9">

                    {message && (
                        <div className={`alert ${isError ? "alert-danger" : "alert-success"}`}>{message}</div>
                    )}

                    {/* Siparişlerim Sekmesi */}
                    {activeTab === "orders" && (
                        <>
                            {/* 🎯 KRİTİK: TALEP FORMU GÖSTERİMİ */}
                            {orderToReturn ? (
                                <ReturnRequestForm
                                    order={orderToReturn}
                                    onBack={handleBackToOrders}
                                    onSubmit={handleReturnSubmit}
                                    isSubmitting={submitting}
                                />
                            ) : selectedOrderId ? (
                                // Sipariş Detay Görünümü
                                <OrderDetail
                                    orderId={selectedOrderId}
                                    onBack={handleBackToOrders}
                                    onCancel={handleCancelOrder}
                                    onRequestReturn={handleRequestReturn}
                                    isSubmitting={submitting}
                                    getStatusBadge={getStatusBadge}
                                    orderDetail={currentOrderDetail} // Detay verisini gönderiyoruz
                                />
                            ) : (
                                // Sipariş Listesi Görünümü
                                <div className="card border-0 shadow-sm">
                                    <div className="card-header bg-white py-3 border-bottom-0">
                                        <h5 className="m-0 fw-bold">Siparişlerim ({orders.length})</h5>
                                    </div>

                                    {ordersLoading ? (
                                        <div className="text-center py-5">
                                            <Loader size={32} className="spinner-border text-dark" />
                                            <p className="mt-3 text-muted">Siparişler yükleniyor...</p>
                                        </div>
                                    ) : (
                                        <div className="table-responsive">
                                            <table className="table table-hover align-middle">
                                                <thead className="table-light">
                                                    <tr>
                                                        <th className="ps-4">No</th>
                                                        <th>Tarih</th>
                                                        <th>Tutar</th>
                                                        <th>Durum</th>
                                                        <th className="text-end pe-4">Detay</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {orders.length > 0 ? (
                                                        orders.map((order) => (
                                                            <tr
                                                                key={order.OrderID}
                                                                onClick={() => handleOrderClick(order.OrderID)}
                                                                style={{ cursor: "pointer" }}
                                                            >
                                                                <td className="ps-4 fw-bold">#{order.OrderID}</td>
                                                                <td>{new Date(order.OrderDate).toLocaleDateString('tr-TR')}</td>
                                                                <td className="fw-bold text-success">₺{parseFloat(order.TotalAmount).toLocaleString()}</td>
                                                                <td>{getStatusBadge(order.Status)}</td>
                                                                <td className="text-end pe-4">
                                                                    <button className="btn btn-sm btn-outline-dark" onClick={(e) => { e.stopPropagation(); handleOrderClick(order.OrderID); }}>
                                                                        Detay
                                                                    </button>
                                                                </td>
                                                            </tr>
                                                        ))
                                                    ) : (
                                                        <tr>
                                                            <td colSpan="5" className="text-center py-5 text-muted">
                                                                <ShoppingBag size={48} className="mb-3 opacity-25" />
                                                                <p className="mb-0">Henüz hiç sipariş vermediniz.</p>
                                                            </td>
                                                        </tr>
                                                    )}
                                                </tbody>
                                            </table>
                                        </div>
                                    )}
                                </div>
                            )}
                        </>
                    )}

                    {/* BİLGİLER Sekmesi (Aynı kaldı) */}
                    {activeTab === "info" && (
                        <>
                            <div className="card p-4 shadow-sm border-0 mb-4">
                                <h4 className="fw-bold mb-4 border-bottom pb-2">
                                    <MapPin className="me-2" /> Bilgilerim
                                </h4>

                                <form onSubmit={handleInfoSubmit} className="row g-3">
                                    <div className="col-md-6">
                                        <label className="form-label">Email</label>
                                        <input
                                            type="email"
                                            name="Email"
                                            value={userData.Email}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Telefon</label>
                                        <input
                                            type="tel"
                                            name="Phone"
                                            value={userData.Phone}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                        />
                                    </div>
                                    <div className="col-12">
                                        <label className="form-label">Adres</label>
                                        <textarea
                                            name="Address"
                                            value={userData.Address}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                            rows="3"
                                        ></textarea>
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Şehir</label>
                                        <input
                                            type="text"
                                            name="City"
                                            value={userData.City}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Ülke</label>
                                        <input
                                            type="text"
                                            name="Country"
                                            value={userData.Country}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                        />
                                    </div>
                                    <div className="col-12 text-end">
                                        <button className="btn btn-dark px-4" disabled={submitting}>
                                            {submitting ? "Güncelleniyor..." : "Güncelle"}
                                        </button>
                                    </div>
                                </form>
                            </div>
                            <div className="card p-4 shadow-sm border-0">
                                <h4 className="fw-bold mb-4 border-bottom pb-2">
                                    <KeyRound className="me-2" /> Şifre Değiştir
                                </h4>

                                <form onSubmit={handlePasswordSubmit} className="row g-3">
                                    <div className="col-md-12">
                                        <label className="form-label">Mevcut Şifre</label>
                                        <input
                                            type="password"
                                            name="currentPassword"
                                            value={passwordData.currentPassword}
                                            onChange={handlePasswordChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Yeni Şifre</label>
                                        <input
                                            type="password"
                                            name="newPassword"
                                            value={passwordData.newPassword}
                                            onChange={handlePasswordChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>
                                    <div className="col-md-6">
                                        <label className="form-label">Yeni Şifre (Tekrar)</label>
                                        <input
                                            type="password"
                                            name="confirmNewPassword"
                                            value={passwordData.confirmNewPassword}
                                            onChange={handlePasswordChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>
                                    <div className="col-12 text-end">
                                        <button className="btn btn-warning px-4" disabled={submitting}>
                                            {submitting ? "Değiştiriliyor..." : "Şifreyi Değiştir"}
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile; 