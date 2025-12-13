import React, { useState, useEffect } from 'react';
import { Package, ShoppingBag, Trash2, Plus, LayoutDashboard, RefreshCw, UploadCloud, Tag, Building, Truck, Send, CheckCircle, XCircle, FileText, User } from 'lucide-react'; 
import api from '../api';

const Admin = () => {
    const [activeTab, setActiveTab] = useState('orders'); 
    const [products, setProducts] = useState([]);
    const [orders, setOrders] = useState([]);
    const [brands, setBrands] = useState([]); 
    const [returnRequests, setReturnRequests] = useState([]); 
    
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false); 
    
    // --- YENİ DETAY STATE'LERİ ---
    const [showOrderDetailModal, setShowOrderDetailModal] = useState(false);
    const [selectedOrder, setSelectedOrder] = useState(null);

    const [showReturnDetailModal, setShowReturnDetailModal] = useState(false);
    const [selectedReturn, setSelectedReturn] = useState(null);
    // ----------------------------

    // --- MARKA EKLEME STATE'LERİ (Aynı Kaldı) ---
    const [newBrandData, setNewBrandData] = useState({
        BrandName: '', Country: '', Description: '',
    });
    const [brandMessage, setBrandMessage] = useState('');
    const [brandError, setBrandError] = useState(false);

    // --- ÜRÜN EKLEME STATE'LERİ (Aynı Kaldı) ---
    const [newProduct, setNewProduct] = useState({
        ModelName: '', Price: '', Stock: '', ImageUrl: '',
        Gender: 'Erkek', BrandID: 1, CaseMaterial: 'Paslanmaz Çelik',
        StrapMaterial: 'Deri', MovementType: 'Otomatik',
        WaterResistance: '5 ATM', Description: '', 
    });
    const [galleryUrls, setGalleryUrls] = useState([]);

    // --- YARDIMCI FONKSİYON: Durum Etiketi ---
    const getStatusBadge = (status) => {
        switch (status) {
            case 'Teslim Edildi':
                return <span className="badge bg-success">Teslim Edildi</span>;
            case 'Tamamlandı':
                return <span className="badge bg-success">İade&Değişim Tamamlandı</span>;
            case 'Onaylandı':
                return <span className="badge bg-success">Onaylandı</span>;
            case 'Kargoda':
                return <span className="badge bg-primary">Kargoda</span>;
            case 'İptal Edildi':
                return <span className="badge bg-danger">İptal Edildi</span>;
            case 'Reddedildi':
                return <span className="badge bg-danger">Reddedildi</span>;
            case 'Beklemede':
            case 'Hazırlanıyor':
            default:
                return <span className="badge bg-warning text-dark">{status}</span>;
        }
    };

    // --- DETAY GÖRÜNTÜLEME FONKSİYONLARI ---
    const showOrderDetails = (order) => {
        setSelectedOrder(order);
        setShowOrderDetailModal(true);
    };

    const showReturnDetails = (request) => {
        setSelectedReturn(request);
        setShowReturnDetailModal(true);
    };

    // --- VERİ ÇEKME (Watches, Orders, Brands, Returns) ---
    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [prodRes, orderRes, brandsRes, returnsRes] = await Promise.all([
                api.get('/api/v1/watches/'),
                api.get('/api/v1/orders/admin/all'), 
                api.get('/api/v1/brands/'),
                api.get('/api/v1/returns/admin/all') 
            ]);

            setProducts(prodRes.data);
            // Sipariş ID'leri büyük harfle (OrderID) geldiği için sıralama bu şekilde
            setOrders(orderRes.data.sort((a, b) => b.OrderID - a.OrderID)); 
            setBrands(brandsRes.data); 
            setReturnRequests(returnsRes.data.sort((a, b) => b.ReturnID - a.ReturnID)); 

            if (brandsRes.data.length > 0) {
                setNewProduct(prev => ({ ...prev, BrandID: brandsRes.data[0].BrandID }));
            }
        } catch (err) {
            console.error("Admin verileri çekilemedi:", err);
            if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                alert("Yetkiniz yok veya oturumunuz sona erdi. Lütfen tekrar giriş yapın.");
            }
        } finally {
            setLoading(false);
        }
    };

    // --- SİPARİŞ DURUMU GÜNCELLEME ---
    const handleStatusUpdate = async (orderId, newStatus) => {
        if (!window.confirm(`Sipariş #${orderId} durumunu "${newStatus}" olarak güncellemek istediğinize emin misiniz?`)) return;

        setSubmitting(true);

        try {
            const payload = { "Status": newStatus }; 
            const response = await api.patch(`/api/v1/orders/admin/${orderId}/status`, payload);
            const updatedOrder = response.data; 

            setOrders(prevOrders => prevOrders.map(order => 
                order.OrderID === orderId ? updatedOrder : order 
            ).sort((a, b) => b.OrderID - a.OrderID)); 
            
            // Modal açıksa, güncel veriyi orada da gösterelim
            if (selectedOrder && selectedOrder.OrderID === orderId) {
                setSelectedOrder(updatedOrder);
            }

            console.log(`Sipariş #${orderId} durumu başarıyla "${newStatus}" olarak güncellendi.`);
            
        } catch (err) {
            console.error("Durum güncelleme hatası:", err.response?.data || err);
            alert(`Durum güncelleme başarısız: ${err.response?.data?.detail || err.message || 'Bilinmeyen bir hata oluştu.'}`);
        } finally {
            setSubmitting(false);
        }
    };
    
    // --- İADE TALEBİ DURUM GÜNCELLEME ---
    const handleReturnStatusUpdate = async (returnId, newStatus) => {
        if (!window.confirm(`Talep #${returnId} durumunu "${newStatus}" olarak güncellemek istediğinize emin misiniz?`)) return;

        setSubmitting(true);

        try {
            const payload = { "Status": newStatus };
            const response = await api.patch(`/api/v1/returns/admin/${returnId}/status`, payload);
            const updatedRequest = response.data;

            setReturnRequests(prevRequests => prevRequests.map(req => 
                req.ReturnID === returnId ? updatedRequest : req
            ).sort((a, b) => b.ReturnID - a.ReturnID));

            // Modal açıksa, güncel veriyi orada da gösterelim
            if (selectedReturn && selectedReturn.ReturnID === returnId) {
                setSelectedReturn(updatedRequest);
            }

            alert(`Talep #${returnId} başarıyla "${newStatus}" olarak güncellendi.`);

        } catch (err) {
            console.error("İade durumu güncelleme hatası:", err.response?.data || err);
            alert(`Güncelleme başarısız: ${err.response?.data?.detail || err.message || 'Bilinmeyen bir hata oluştu.'}`);
        } finally {
            setSubmitting(false);
        }
    };


    // --- Diğer form ve delete fonksiyonları (Aynı Kaldı) ---
    const handleProductChange = (e) => {
        const { name, value } = e.target;
        setNewProduct(prev => ({ ...prev, [name]: value }));
    };

    const handleBrandFormChange = (e) => {
        const { name, value } = e.target;
        setNewBrandData(prev => ({ ...prev, [name]: value }));
    };

    const handleAddBrandSubmit = async (e) => {
        e.preventDefault();
        setBrandMessage(''); setBrandError(false);
        if (!newBrandData.BrandName || !newBrandData.Country || !newBrandData.Description) { setBrandMessage('Lütfen tüm alanları doldurun.'); setBrandError(true); return; }
        setSubmitting(true);
        try {
            await api.post('/api/v1/brands/', newBrandData); 
            setBrandMessage(`"${newBrandData.BrandName}" başarıyla eklendi!`);
            setBrandError(false);
            setNewBrandData({ BrandName: '', Country: '', Description: '' });
            fetchData(); 
        } catch (err) {
            console.error("Marka eklenirken hata oluştu:", err);
            const errMsg = err.response?.data?.detail || 'Marka eklenirken bir hata oluştu.';
            setBrandMessage(`HATA: ${errMsg}`);
            setBrandError(true);
        } finally { setSubmitting(false); }
    };
    
    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        try {
            const response = await api.post('/api/v1/upload/', formData, { headers: { 'Content-Type': 'multipart/form-data' }, });
            setNewProduct(prev => ({ ...prev, ImageUrl: response.data.url }));
        } catch (err) { console.error("Kapak resmi hatası:", err); alert("Kapak resmi yüklenirken hata oluştu."); }
    };

    const handleGalleryUpload = async (e) => {
        const files = Array.from(e.target.files);
        if (files.length === 0) return;
        const uploadPromises = files.map(file => {
            const formData = new FormData();
            formData.append('file', file);
            return api.post('/api/v1/upload/', formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        });
        try {
            const responses = await Promise.all(uploadPromises);
            const uploadedUrls = responses.map(res => res.data.url);
            setGalleryUrls(prev => [...prev, ...uploadedUrls]);
        } catch (err) { console.error("Galeri yükleme hatası:", err); alert("Bazı resimler yüklenemedi."); }
    };

    const handleAddSubmit = async (e) => {
        e.preventDefault();
        if (!newProduct.ModelName || !newProduct.Price || !newProduct.Stock || !newProduct.BrandID || !newProduct.CaseMaterial || !newProduct.StrapMaterial || !newProduct.MovementType || !newProduct.WaterResistance) { alert("Lütfen Model Adı, Fiyat, Stok ve tüm Teknik Detayları girin!"); return; }
        setSubmitting(true);

        try {
            const payload = {
                ModelName: newProduct.ModelName, Price: parseFloat(newProduct.Price),
                Stock: parseInt(newProduct.Stock), ImageUrl: newProduct.ImageUrl || "https://via.placeholder.com/300",
                BrandID: parseInt(newProduct.BrandID), Gender: newProduct.Gender, 
                CaseMaterial: newProduct.CaseMaterial, StrapMaterial: newProduct.StrapMaterial,
                MovementType: newProduct.MovementType, WaterResistance: newProduct.WaterResistance,
                Description: newProduct.Description,
            };

            const response = await api.post('/api/v1/watches/', payload);
            const createdWatchID = response.data.WatchID || response.data.id;

            if (galleryUrls.length > 0) {
                await Promise.all(galleryUrls.map(url => api.post('/api/v1/watches/watch_images/', { WatchID: createdWatchID, ImageUrl: url })));
            }

            alert("Ürün başarıyla eklendi! 🎉");
            setNewProduct(prev => ({ 
                ...prev, ModelName: '', Price: '', Stock: '', ImageUrl: '', Description: '', 
                BrandID: brands.length > 0 ? brands[0].BrandID : 1
            }));
            setGalleryUrls([]);
            fetchData(); 
        } catch (err) {
            console.error("Ekleme hatası:", err.response?.data || err);
            alert(`Ürün eklenirken hata oluştu: ${err.response?.data?.detail || err.message}`);
        } finally {
            setSubmitting(false);
        }
    };

    const handleRemoveProduct = async (id) => {
        if (!window.confirm("Bu ürünü silmek istediğine emin misin?")) return;
        try {
            await api.delete(`/api/v1/watches/${id}`);
            setProducts(products.filter(p => p.WatchID !== id));
        } catch (err) {
            console.error("Silme hatası:", err);
            alert("Silme işlemi başarısız.");
        }
    };


    if (loading) return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="spinner-border text-warning" role="status">
                <span className="visually-hidden">Yükleniyor...</span>
            </div>
        </div>
    );

    return (
        <div className="container py-5">
            
            {/* Üst Başlık ve Yenile Butonu */}
            <div className="d-flex align-items-center justify-content-between mb-4">
                <div className="d-flex align-items-center text-warning">
                    <LayoutDashboard size={32} className="me-2" />
                    <h2 className="fw-bold m-0 text-dark">Yönetim Paneli</h2>
                </div>
                <button onClick={fetchData} className="btn btn-outline-dark btn-sm rounded-pill px-3" disabled={submitting}>
                    <RefreshCw size={16} className="me-1" /> Yenile
                </button>
            </div>

            <div className="row">
                {/* Sol Menü */}
                <div className="col-md-3 mb-4">
                    <div className="list-group shadow-sm border-0">
                        <button
                            className={`list-group-item list-group-item-action border-0 d-flex align-items-center py-3 ${activeTab === 'products' ? 'active bg-dark text-white fw-bold' : ''}`}
                            onClick={() => setActiveTab('products')}
                        >
                            <Package size={18} className="me-2" /> Ürün Yönetimi
                        </button>
                        
                        <button
                            className={`list-group-item list-group-item-action border-0 d-flex align-items-center py-3 ${activeTab === 'brands' ? 'active bg-dark text-white fw-bold' : ''}`}
                            onClick={() => setActiveTab('brands')}
                        >
                            <Tag size={18} className="me-2" /> Marka Yönetimi
                        </button>

                        <button
                            className={`list-group-item list-group-item-action border-0 d-flex align-items-center py-3 ${activeTab === 'orders' ? 'active bg-dark text-white fw-bold' : ''}`}
                            onClick={() => setActiveTab('orders')}
                        >
                            <ShoppingBag size={18} className="me-2" /> Siparişler ({orders.length})
                        </button>
                        
                        <button
                            className={`list-group-item list-group-item-action border-0 d-flex align-items-center py-3 ${activeTab === 'returns' ? 'active bg-dark text-white fw-bold' : ''}`}
                            onClick={() => setActiveTab('returns')}
                        >
                            <Tag size={18} className="me-2" /> İade/Değişim ({returnRequests.length})
                        </button>
                    </div>
                </div>

                {/* İçerik Alanı */}
                <div className="col-md-9">

                    {/* --- 1. MARKA YÖNETİMİ --- */}
                    {activeTab === 'brands' && (
                        <div className="card shadow-sm p-4">
                            <h4 className="fw-bold mb-4 border-bottom pb-2">Yeni Marka Ekle</h4>
                            
                            {brandMessage && (
                                <div className={`alert ${brandError ? 'alert-danger' : 'alert-success'} mb-4`} role="alert">
                                    {brandMessage}
                                </div>
                            )}

                            <form onSubmit={handleAddBrandSubmit}>
                                <div className="mb-3">
                                    <label htmlFor="BrandName" className="form-label fw-bold">Marka Adı *</label>
                                    <input type="text" className="form-control" id="BrandName" name="BrandName" value={newBrandData.BrandName} onChange={handleBrandFormChange} required placeholder="Örn: Casio, Seiko, Rolex" />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="Country" className="form-label fw-bold">Ülke *</label>
                                    <input type="text" className="form-control" id="Country" name="Country" value={newBrandData.Country} onChange={handleBrandFormChange} required placeholder="Örn: Japonya, İsviçre" />
                                </div>
                                <div className="mb-4">
                                    <label htmlFor="Description" className="form-label fw-bold">Açıklama *</label>
                                    <textarea className="form-control" id="Description" name="Description" rows="3" value={newBrandData.Description} onChange={handleBrandFormChange} required placeholder="Markanın kısa tanıtımını yapın."></textarea>
                                </div>

                                <button type="submit" className="btn btn-dark w-100 fw-bold rounded-pill" disabled={submitting}>
                                    {submitting ? "Kaydediliyor..." : (<><Building size={18} className="me-1 mb-1" /> Markayı Kaydet</>)}
                                </button>
                            </form>
                            
                            <h5 className="fw-bold mt-5 mb-3 border-bottom pb-2">Mevcut Markalar ({brands.length})</h5>
                            {brands.length > 0 ? (
                                <ul className="list-group list-group-flush">
                                    {brands.map(brand => (
                                        <li key={brand.BrandID} className="list-group-item d-flex justify-content-between align-items-center">
                                            {brand.BrandName} ({brand.Country})
                                            <span className="badge bg-secondary">{brand.BrandID}</span>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="text-muted">Henüz hiç marka eklenmedi.</p>
                            )}
                        </div>
                    )}


                    {/* --- 2. ÜRÜN YÖNETİMİ --- */}
                    {activeTab === 'products' && (
                        <>
                            <div className="card border-0 shadow-sm mb-4">
                                <div className="card-header bg-white py-3 border-bottom-0">
                                    <h5 className="m-0 fw-bold text-dark">Yeni Ürün Ekle</h5>
                                </div>
                                <div className="card-body">
                                    <form onSubmit={handleAddSubmit} className="row g-3">
                                        
                                        {/* Row 1: Temel Bilgiler */}
                                        <div className="col-md-6">
                                            <label className="form-label small text-muted fw-bold">Model Adı *</label>
                                            <input type="text" className="form-control bg-light border-0" name="ModelName" value={newProduct.ModelName} onChange={handleProductChange} required />
                                        </div>
                                        <div className="col-md-3">
                                            <label className="form-label small text-muted fw-bold">Fiyat (₺) *</label>
                                            <input type="number" className="form-control bg-light border-0" name="Price" value={newProduct.Price} onChange={handleProductChange} required />
                                        </div>
                                        <div className="col-md-3">
                                            <label className="form-label small text-muted fw-bold">Stok *</label>
                                            <input type="number" className="form-control bg-light border-0" name="Stock" value={newProduct.Stock} onChange={handleProductChange} required placeholder="10" />
                                        </div>

                                        <h6 className="mt-4 text-muted border-bottom pb-1">Teknik Detaylar</h6>
                                        
                                        {/* Row 2: Teknik Detaylar */}
                                        <div className="col-md-3">
                                            <label className="form-label small text-muted fw-bold">Kasa Materyali *</label>
                                            <select className="form-select bg-light border-0" name="CaseMaterial" value={newProduct.CaseMaterial} onChange={handleProductChange} required>
                                                <option value="Paslanmaz Çelik">Paslanmaz Çelik</option>
                                                <option value="Titanyum">Titanyum</option>
                                                <option value="Altın Kaplama">Altın Kaplama</option>
                                                <option value="Seramik">Seramik</option>
                                                <option value="Polimer">Polimer</option>
                                            </select>
                                        </div>
                                        <div className="col-md-3">
                                            <label className="form-label small text-muted fw-bold">Kayış Materyali *</label>
                                            <select className="form-select bg-light border-0" name="StrapMaterial" value={newProduct.StrapMaterial} onChange={handleProductChange} required>
                                                <option value="Deri">Deri</option>
                                                <option value="Çelik">Çelik</option>
                                                <option value="Silikon">Silikon</option>
                                                <option value="Kumaş">Kumaş</option>
                                                <option value="Hasır">Hasır</option>
                                            </select>
                                        </div>
                                        <div className="col-md-3">
                                            <label className="form-label small text-muted fw-bold">Mekanizma Tipi *</label>
                                            <select className="form-select bg-light border-0" name="MovementType" value={newProduct.MovementType} onChange={handleProductChange} required>
                                                <option value="Otomatik">Otomatik</option>
                                                <option value="Quartz">Quartz</option>
                                                <option value="Manuel">Manuel</option>
                                            </select>
                                        </div>
                                        <div className="col-md-3">
                                            <label className="form-label small text-muted fw-bold">Su Direnci *</label>
                                            <select className="form-select bg-light border-0" name="WaterResistance" value={newProduct.WaterResistance} onChange={handleProductChange} required>
                                                <option value="3 ATM">3 ATM (Sıçrama)</option>
                                                <option value="5 ATM">5 ATM (Duş)</option>
                                                <option value="10 ATM">10 ATM (Yüzme)</option>
                                                <option value="20 ATM+">20 ATM+ (Dalış)</option>
                                            </select>
                                        </div>
                                        
                                        {/* Row 3: Marka, Kategori, Açıklama */}
                                        <div className="col-md-4">
                                            <label className="form-label small text-muted fw-bold">Marka Seçimi *</label>
                                            <select className="form-select bg-light border-0" name="BrandID" value={newProduct.BrandID} onChange={handleProductChange} required disabled={brands.length === 0}>
                                                {brands.length === 0 ? (
                                                    <option value="">Önce Marka Ekleyin (Marka Yönetimi)</option>
                                                ) : (
                                                    brands.map(brand => (
                                                        <option key={brand.BrandID} value={brand.BrandID}>
                                                            {brand.BrandName}
                                                        </option>
                                                    ))
                                                )}
                                            </select>
                                        </div>
                                        <div className="col-md-4">
                                            <label className="form-label small text-muted fw-bold">Cinsiyet *</label>
                                            <select className="form-select bg-light border-0" name="Gender" value={newProduct.Gender} onChange={handleProductChange}>
                                                <option value="Erkek">Erkek</option>
                                                <option value="Kadın">Kadın</option>
                                                <option value="Çocuk">Çocuk</option>
                                            </select>
                                        </div>
                                        <div className="col-md-4">
                                            <label className="form-label small text-muted fw-bold">Açıklama (Opsiyonel)</label>
                                            <input type="text" className="form-control bg-light border-0" name="Description" value={newProduct.Description} onChange={handleProductChange} placeholder="Saat hakkında kısa bilgi" />
                                        </div>

                                        {/* Row 4: Resim Yükleme Alanları */}
                                        <div className="col-md-6">
                                            <label className="form-label small text-muted fw-bold">Kapak Görseli</label>
                                            <div className="input-group">
                                                <label className="input-group-text bg-white border-end-0 cursor-pointer">
                                                    <UploadCloud size={18} />
                                                </label>
                                                <input type="file" className="form-control bg-light border-start-0" onChange={handleFileUpload} accept="image/*" />
                                            </div>
                                            {newProduct.ImageUrl && (
                                                <div className="mt-2">
                                                    <img src={newProduct.ImageUrl} alt="Kapak" style={{ height: '50px', borderRadius: '5px', objectFit: 'cover' }} />
                                                </div>
                                            )}
                                        </div>

                                        <div className="col-md-6">
                                            <label className="form-label small text-muted fw-bold">Galeri (Çoklu)</label>
                                            <div className="input-group">
                                                <label className="input-group-text bg-white border-end-0">
                                                    <UploadCloud size={18} />
                                                </label>
                                                <input type="file" className="form-control bg-light border-start-0" onChange={handleGalleryUpload} accept="image/*" multiple />
                                            </div>
                                            <div className="d-flex gap-2 mt-2 flex-wrap">
                                                {galleryUrls.map((url, index) => (
                                                    <img key={index} src={url} alt={`Galeri ${index}`} style={{ height: '40px', width: '40px', borderRadius: '4px', objectFit: 'cover', border: '1px solid #eee' }} />
                                                ))}
                                            </div>
                                        </div>

                                        <div className="col-12 text-end mt-4">
                                            <button
                                                type="submit"
                                                className="btn btn-warning fw-bold px-4 shadow-sm"
                                                disabled={submitting || brands.length === 0} 
                                            >
                                                {submitting ? (
                                                    <>Kaydediliyor...</>
                                                ) : (
                                                    <><Plus size={18} className="me-1 mb-1" /> Kaydet</>
                                                )}
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                            
                            {/* Mevcut Ürünler Listesi */}
                            <div className="card border-0 shadow-sm">
                                <div className="card-header bg-white py-3 border-bottom-0">
                                    <h5 className="m-0 fw-bold text-dark">Ürün Listesi ({products.length})</h5>
                                </div>
                                <div className="table-responsive" style={{ maxHeight: '500px' }}>
                                    <table className="table table-hover align-middle mb-0">
                                        <thead className="table-light sticky-top">
                                            <tr>
                                                <th className="ps-4">Görsel</th>
                                                <th>Model</th>
                                                <th>Kategori</th>
                                                <th>Marka ID</th>
                                                <th>Stok</th>
                                                <th>Fiyat</th>
                                                <th className="text-end pe-4">İşlem</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {products.map(product => (
                                                <tr key={product.WatchID}>
                                                    <td className="ps-4">
                                                        <img src={product.ImageUrl || "https://via.placeholder.com/40"} alt="img" style={{ width: '40px', height: '40px', objectFit: 'contain' }} className="bg-light rounded border" />
                                                    </td>
                                                    <td className="fw-bold">{product.ModelName}</td>
                                                    <td><span className="badge bg-secondary fw-normal">{product.Gender}</span></td>
                                                    <td>{product.BrandID}</td>
                                                    <td>
                                                        <span className={`badge ${product.Stock < 5 ? 'bg-danger' : 'bg-light text-dark border'}`}>
                                                            {product.Stock}
                                                        </span>
                                                    </td>
                                                    <td>₺{product.Price?.toLocaleString()}</td>
                                                    <td className="text-end pe-4">
                                                        <button className="btn btn-sm btn-light text-danger border-0" onClick={() => handleRemoveProduct(product.WatchID)} title="Ürünü Sil">
                                                            <Trash2 size={18} />
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                        </>
                    )}

                    {/* --- 3. SİPARİŞLER --- */}
                    {activeTab === 'orders' && (
                        <div className="card border-0 shadow-sm">
                            <div className="card-header bg-white py-3 border-bottom-0">
                                <h5 className="m-0 fw-bold">Gelen Siparişler</h5>
                            </div>
                            <div className="table-responsive">
                                <table className="table table-hover align-middle mb-0">
                                    <thead className="table-light">
                                        <tr>
                                            <th className="ps-4">Sipariş No</th>
                                            <th>Kullanıcı ID</th> 
                                            <th>Tarih</th>
                                            <th>Tutar</th>
                                            <th>Durum</th>
                                            <th className="text-end pe-4">İşlem</th> 
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {orders.length > 0 ? orders.map(order => (
                                            <tr key={order.OrderID}>
                                                <td className="ps-4 fw-bold">#{order.OrderID}</td>
                                                <td>{order.UserID}</td> 
                                                <td>{new Date(order.OrderDate).toLocaleDateString('tr-TR')}</td>
                                                <td className="fw-bold text-success">₺{parseFloat(order.TotalAmount).toLocaleString()}</td>
                                                <td>
                                                    {getStatusBadge(order.Status)}
                                                </td>
                                                <td className="text-end pe-4">
                                                    {/* YENİ DETAY BUTONU */}
                                                    <button 
                                                        className="btn btn-sm btn-outline-secondary me-2" 
                                                        onClick={() => showOrderDetails(order)}
                                                        title="Sipariş Detaylarını Gör"
                                                    >
                                                        <FileText size={16} /> Detay
                                                    </button>
                                                    
                                                    {/* EYLEM BUTONLARI */}
                                                    {order.Status === 'Hazırlanıyor' && (
                                                        <button 
                                                            className="btn btn-sm btn-outline-primary" 
                                                            onClick={() => handleStatusUpdate(order.OrderID, 'Kargoda')}
                                                            disabled={submitting}
                                                            title="Siparişi kargoya ver"
                                                        >
                                                            <Truck size={16} /> Kargola
                                                        </button>
                                                    )}
                                                     {order.Status === 'Kargoda' && ( 
                                                         <button 
                                                             className="btn btn-sm btn-outline-success" 
                                                             onClick={() => handleStatusUpdate(order.OrderID, 'Teslim Edildi')}
                                                             disabled={submitting}
                                                             title="Siparişi teslim edildi olarak işaretle"
                                                         >
                                                             Teslim Edildi
                                                         </button>
                                                     )}
                                                </td>
                                            </tr>
                                        )) : (
                                            <tr><td colSpan="6" className="text-center py-5 text-muted">Henüz hiç sipariş yok.</td></tr>
                                        )}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                    
                    {/* --- 4. İADE/DEĞİŞİM TALEPLERİ --- */}
                    {activeTab === 'returns' && (
                       <div className="card shadow-sm p-4">
                            <h4 className="fw-bold mb-4">İade & Değişim Talepleri ({returnRequests.length})</h4>
                            
                            {returnRequests.length > 0 ? (
                                <div className="table-responsive">
                                    <table className="table table-hover align-middle">
                                        <thead className="table-light">
                                            <tr>
                                                <th>Talep No</th>
                                                <th>Sipariş No</th>
                                                <th>Ürün Adı</th> {/* YENİ: Ürün Adı Kolonu */}
                                                <th>Tip</th>
                                                <th>Neden</th>
                                                <th>Durum</th>
                                                <th className="text-end">İşlemler</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {returnRequests.map(req => (
                                                <tr key={req.ReturnID}>
                                                    <td className="fw-bold">#{req.ReturnID}</td>
                                                    <td>#{req.OrderID}</td>
                                                    {/* ÜRÜN ADI GÖSTERİMİ */}
                                                    <td>
                                                        {req.order?.order_details?.length > 0 ? (
                                                            // İlk ürünün adını alıyoruz
                                                            `${req.order.order_details[0].watch?.brand?.BrandName || ''} ${req.order.order_details[0].watch?.ModelName || 'Model Adı Yok'}`
                                                        ) : (
                                                            'Ürün Detayı Yok'
                                                        )}
                                                    </td>
                                                    <td>{req.RequestType}</td>
                                                    <td title={req.Description || req.Reason}>{req.Reason.substring(0, 20)}...</td>
                                                    <td>{getStatusBadge(req.Status)}</td>
                                                    <td className="text-end">
                                                        {/* YENİ DETAY BUTONU */}
                                                        <button 
                                                            className="btn btn-sm btn-outline-secondary me-2" 
                                                            onClick={() => showReturnDetails(req)}
                                                            title="İade Detaylarını Gör"
                                                        >
                                                            <FileText size={16} /> Detay
                                                        </button>
                                                        
                                                        {/* İŞLEM BUTONLARI */}
                                                        {req.Status === 'Beklemede' && (
                                                            <>
                                                                <button 
                                                                    className="btn btn-sm btn-success me-2" 
                                                                    onClick={() => handleReturnStatusUpdate(req.ReturnID, 'Onaylandı')}
                                                                    disabled={submitting}
                                                                    title="Talebi Onayla"
                                                                >
                                                                    <CheckCircle size={16} />
                                                                </button>
                                                                <button 
                                                                    className="btn btn-sm btn-danger" 
                                                                    onClick={() => handleReturnStatusUpdate(req.ReturnID, 'Reddedildi')}
                                                                    disabled={submitting}
                                                                    title="Talebi Reddet"
                                                                >
                                                                    <XCircle size={16} />
                                                                </button>
                                                            </>
                                                        )}
                                                        {req.Status === 'Onaylandı' && (
                                                            <button 
                                                                className="btn btn-sm btn-primary" 
                                                                onClick={() => handleReturnStatusUpdate(req.ReturnID, 'Tamamlandı')}
                                                                disabled={submitting}
                                                                title="İşlemi Tamamlandı"
                                                            >
                                                                Tamamla
                                                            </button>
                                                        )}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            ) : (
                                <p className="text-muted">Şu anda aktif iade veya değişim talebi bulunmamaktadır.</p>
                            )}
                       </div>
                    )}
                </div>
            </div>

            {/* --- MODAL BİLEŞENLERİNİ ÇAĞIRMA --- */}
            {showOrderDetailModal && selectedOrder && (
                <OrderDetailsModal 
                    order={selectedOrder} 
                    onClose={() => setShowOrderDetailModal(false)} 
                    getStatusBadge={getStatusBadge}
                    handleStatusUpdate={handleStatusUpdate}
                    submitting={submitting}
                />
            )}

            {showReturnDetailModal && selectedReturn && (
                <ReturnDetailsModal 
                    request={selectedReturn} 
                    onClose={() => setShowReturnDetailModal(false)} 
                    getStatusBadge={getStatusBadge}
                    handleReturnStatusUpdate={handleReturnStatusUpdate}
                    submitting={submitting}
                />
            )}
        </div>
    );
};

export default Admin;


// --- MODAL BİLEŞENLERİ (Aynı Dosyada VEYA Ayrı Bir Dosyada Tanımlanabilir) ---

// 1. SİPARİŞ DETAY MODALI
const OrderDetailsModal = ({ order, onClose, getStatusBadge, handleStatusUpdate, submitting }) => {
    return (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
            <div className="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                <div className="modal-content">
                    <div className="modal-header bg-dark text-white">
                        <h5 className="modal-title">Sipariş Detayları #{order.OrderID}</h5>
                        <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
                    </div>
                    <div className="modal-body">
                        <div className="row">
                            <div className="col-md-6">
                                <h6><ShoppingBag size={18} className="me-1 mb-1" /> **Genel Bilgiler**</h6>
                                <p><strong>Durum:</strong> {getStatusBadge(order.Status)}</p>
                                <p><strong>Tutar:</strong> ₺{parseFloat(order.TotalAmount).toLocaleString()}</p>
                                <p><strong>Tarih:</strong> {new Date(order.OrderDate).toLocaleDateString('tr-TR')}</p>
                            </div>
                            <div className="col-md-6">
                                <h6><User size={18} className="me-1 mb-1" /> **Kullanıcı & Adres**</h6>
                                <p><strong>Kullanıcı ID:</strong> {order.UserID}</p>
                                <p><strong>Teslimat Adresi:</strong> {order.ShippingAddress}</p>
                            </div>
                        </div>
                        
                        <hr />
                        <h6><Package size={18} className="me-1 mb-1" /> **Ürünler ({order.order_details.length})**</h6>
                        <ul className="list-group list-group-flush">
                            {order.order_details.map(detail => (
                                <li key={detail.OrderDetailID || detail.id} className="list-group-item d-flex justify-content-between align-items-center">
                                    <div className="d-flex align-items-center">
                                        <img src={detail.watch?.ImageUrl || "https://via.placeholder.com/30"} alt="Ürün" style={{ width: '30px', height: '30px', objectFit: 'contain' }} className="me-2 rounded" />
                                        <span>
                                            **{detail.watch?.brand?.BrandName || 'Bilinmiyor'} {detail.watch?.ModelName}**
                                        </span>
                                    </div>
                                    <span className="badge bg-secondary">
                                        {detail.Quantity} x ₺{parseFloat(detail.UnitPrice).toLocaleString()}
                                    </span>
                                </li>
                            ))}
                        </ul>

                    </div>
                    <div className="modal-footer">
                         {/* Durum güncelleme butonları (Modal'dan da erişilebilir) */}
                         {order.Status === 'Hazırlanıyor' && (
                            <button 
                                className="btn btn-primary" 
                                onClick={() => handleStatusUpdate(order.OrderID, 'Kargoda')}
                                disabled={submitting}
                            >
                                <Truck size={16} /> Kargola
                            </button>
                        )}
                        {order.Status === 'Kargoda' && ( 
                            <button 
                                className="btn btn-success" 
                                onClick={() => handleStatusUpdate(order.OrderID, 'Teslim Edildi')}
                                disabled={submitting}
                            >
                                Teslim Edildi
                            </button>
                        )}
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Kapat</button>
                    </div>
                </div>
            </div>
        </div>
    );
};

// 2. İADE DETAY MODALI
const ReturnDetailsModal = ({ request, onClose, getStatusBadge, handleReturnStatusUpdate, submitting }) => {
    // İade objesi artık sipariş detaylarını içeriyor.
    const firstOrderDetail = request.order?.order_details?.[0];

    return (
        <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
            <div className="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
                <div className="modal-content">
                    <div className="modal-header bg-dark text-white">
                        <h5 className="modal-title">İade/Değişim Talebi Detayları #{request.ReturnID}</h5>
                        <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
                    </div>
                    <div className="modal-body">
                        <div className="row">
                            <div className="col-md-6">
                                <h6><FileText size={18} className="me-1 mb-1" /> **Talep Bilgileri**</h6>
                                <p><strong>Durum:</strong> {getStatusBadge(request.Status)}</p>
                                <p><strong>Tip:</strong> {request.RequestType}</p>
                                <p><strong>Talep Tarihi:</strong> {new Date(request.CreatedAt).toLocaleDateString('tr-TR')}</p>
                            </div>
                            <div className="col-md-6">
                                <h6><ShoppingBag size={18} className="me-1 mb-1" /> **İlgili Sipariş**</h6>
                                <p><strong>Sipariş No:</strong> {request.OrderID}</p>
                                <p><strong>Kullanıcı ID:</strong> {request.UserID}</p>
                            </div>
                        </div>
                        
                        <hr />
                        <h6><Package size={18} className="me-1 mb-1" /> **İlgili Ürün**</h6>
                        {/* Not: İade talebi hangi ürüne aitse onun detayını gösteriyoruz. 
                           Eğer talep birden fazla ürünü içeriyorsa, bu kısım tüm ürünleri listelemek için güncellenmeli. 
                           Şimdilik ilk ürünü gösteriyoruz. */}
                        {firstOrderDetail ? (
                             <div className="d-flex align-items-center mb-3 p-2 bg-light rounded">
                                <img src={firstOrderDetail.watch?.ImageUrl || "https://via.placeholder.com/40"} alt="Ürün" style={{ width: '40px', height: '40px', objectFit: 'contain' }} className="me-3 rounded" />
                                <div>
                                    <p className="m-0 fw-bold">{firstOrderDetail.watch?.brand?.BrandName || 'Bilinmiyor'} {firstOrderDetail.watch?.ModelName}</p>
                                    <p className="m-0 small text-muted">Adet: {firstOrderDetail.Quantity} | Fiyat: ₺{parseFloat(firstOrderDetail.UnitPrice).toLocaleString()}</p>
                                </div>
                             </div>
                        ) : (
                            <p className="text-danger">İlgili sipariş detayı bulunamadı.</p>
                        )}

                        <hr />
                        <h6><Send size={18} className="me-1 mb-1" /> **Müşteri Notu**</h6>
                        <p><strong>Neden:</strong> <span className='fw-bold'>{request.Reason}</span></p>
                        <p className={`p-3 ${request.Description ? 'bg-light rounded' : 'text-muted'}`}>
                            {request.Description || "Müşteri detaylı açıklama girmemiş."}
                        </p>

                    </div>
                    <div className="modal-footer">
                        {/* Durum güncelleme butonları (Modal'dan da erişilebilir) */}
                        {request.Status === 'Beklemede' && (
                            <>
                                <button 
                                    className="btn btn-success" 
                                    onClick={() => handleReturnStatusUpdate(request.ReturnID, 'Onaylandı')}
                                    disabled={submitting}
                                >
                                    <CheckCircle size={16} /> Onayla
                                </button>
                                <button 
                                    className="btn btn-danger" 
                                    onClick={() => handleReturnStatusUpdate(request.ReturnID, 'Reddedildi')}
                                    disabled={submitting}
                                >
                                    <XCircle size={16} /> Reddet
                                </button>
                            </>
                        )}
                        {request.Status === 'Onaylandı' && (
                            <button 
                                className="btn btn-primary" 
                                onClick={() => handleReturnStatusUpdate(request.ReturnID, 'Tamamlandı')}
                                disabled={submitting}
                            >
                                Tamamla
                            </button>
                        )}
                        <button type="button" className="btn btn-secondary" onClick={onClose}>Kapat</button>
                    </div>
                </div>
            </div>
        </div>
    );
};