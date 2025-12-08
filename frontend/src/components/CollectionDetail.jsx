import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Watch, ShoppingBag, ArrowLeft, FilterX, Building } from 'lucide-react';
import api from '../api';

const CollectionDetail = () => {

    const [searchParams] = useSearchParams();
    const type = searchParams.get('type');
    const value = searchParams.get('value');

    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [pageTitle, setPageTitle] = useState("Koleksiyon");
    const [isWatches, setIsWatches] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setData([]);
            let watchesEndpoint = ''; // Saatleri veya tüm markaları çeken endpoint
            let currentTitle = "Ürünler";
            let isWatchesData = false;
            let brandId = null; // Marka ID'sini geçici tutmak için

            if (type === 'gender' && value) {
                // --- CİNSİYET FİLTRELEME ---
                currentTitle = `${value} Saatleri Koleksiyonu`;
                isWatchesData = true;
                watchesEndpoint = `/api/v1/watches/by_gender/?gender=${value}`;

            } else if (type === 'brandId' && value) {
                // --- MARKA ID FİLTRELEME (KRİTİK BÖLGE) ---
                isWatchesData = true;
                brandId = value;
                watchesEndpoint = `/api/v1/watches/by_brand/?brand_id=${value}`;
                
                // 🎯 1. Marka Adını Çekme (Başlık için)
                try {
                    // Tek bir markanın detayını çeken endpoint'i kullanıyoruz.
                    // API varsayımı: GET /api/v1/brands/{id} çalışıyor.
                    const brandRes = await api.get(`/api/v1/brands/${brandId}`); 
                    currentTitle = `${brandRes.data.BrandName} Koleksiyonu`;

                } catch (err) {
                    // Eğer marka adı çekilemezse, ID ile devam et.
                    console.error("Marka adı çekilemedi:", err);
                    currentTitle = `Marka Ürünleri (ID: ${brandId})`; 
                }

            } else if (type === 'brands') {
                // --- TÜM MARKALARIN LİSTESİ ---
                currentTitle = "Tüm Markalarımız";
                isWatchesData = false;
                watchesEndpoint = '/api/v1/brands/';

            } else {
                currentTitle = "Koleksiyon Bulunamadı (Geçersiz URL)";
                setLoading(false);
                setPageTitle(currentTitle);
                return;
            }

            setPageTitle(currentTitle);
            setIsWatches(isWatchesData);

            try {
                // 🎯 2. Ana liste (Saat veya Marka listesi) çekilir
                const response = await api.get(watchesEndpoint);
                setData(response.data);
            } catch (err) {
                console.error("Veri yüklenemedi:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [type, value]);

    if (loading) return (
        <div className="d-flex justify-content-center align-items-center py-5" style={{ minHeight: '50vh' }}>
            <div className="spinner-border text-dark" role="status">
                <span className="visually-hidden">Yükleniyor...</span>
            </div>
        </div>
    );

    return (
        <div className="container py-5">
            {/* Üst Başlık ve Geri Dön Butonu */}
            <div className="mb-5 border-bottom pb-3">
                <Link to="/collections" className="text-decoration-none text-muted d-inline-flex align-items-center mb-2 hover-dark">
                    <ArrowLeft size={18} className="me-2" /> Tüm Koleksiyonlar
                </Link>
                <div className="d-flex justify-content-between align-items-end">
                    <div>
                        {/* Başlık artık dinamik Marka Adını içeriyor */}
                        <h2 className="fw-bold display-6 mb-0">{pageTitle}</h2>
                        <p className="text-muted mb-0 mt-2 small">Toplam {data.length} {isWatches ? 'ürün' : 'marka'} listeleniyor.</p>
                    </div>
                </div>
            </div>

            {data.length > 0 ? (
                <div className="row g-4">
                    {data.map((item) => (
                        isWatches ? (
                            // --- SAAT KARTI RENDER EDİLİYOR (MARKALAR İÇİN DE KULLANILIR) ---
                            <div className="col-sm-6 col-md-4 col-lg-3" key={item.WatchID}>
                                <Link to={`/product/${item.WatchID}`} className="text-decoration-none">
                                    <div className="card h-100 border-0 shadow-sm overflow-hidden product-card" style={{ transition: 'transform 0.2s' }}>
                                        <div className="position-relative bg-light d-flex align-items-center justify-content-center p-4" style={{ height: '260px' }}>
                                            {item.ImageUrl ? (
                                                <img src={item.ImageUrl} alt={item.ModelName} style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', mixBlendMode: 'multiply' }} />
                                            ) : (
                                                <Watch size={64} strokeWidth={1} className="text-muted opacity-50" />
                                            )}
                                            {item.Stock < 5 && item.Stock > 0 && (
                                                <span className="position-absolute top-0 end-0 m-2 badge bg-danger rounded-pill small">
                                                    Son {item.Stock}
                                                </span>
                                            )}
                                        </div>
                                        <div className="card-body text-center p-3">
                                            {/* 🔥 YENİ EKLENEN KISIM: Marka Adı (Renk: dark) */}
                                            <p className="text-dark fw-bold mb-1 text-uppercase small">
                                                {item.brand?.BrandName || item.Brand?.BrandName || "MARKA BİLİNMİYOR"}
                                            </p>

                                            <h6 className="card-title fw-bold text-dark text-truncate" title={item.ModelName}>
                                                {item.ModelName}
                                            </h6>
                                            {/* Not: Daha önceki istek üzerine Gender alanı kaldırıldı. */}
                                            {/* <div className="text-muted small mb-2">{item.Gender}</div> */}

                                            <span className="text-dark fs-5 fw-bold">
                                                ₺{parseFloat(item.Price).toLocaleString()}
                                            </span>
                                            <button className="btn btn-dark w-100 rounded-pill mt-3 btn-sm fw-bold">
                                                <ShoppingBag size={16} className="me-2 mb-1" /> İncele
                                            </button>
                                        </div>
                                    </div>
                                </Link>
                            </div>
                        ) : (
                            // --- MARKA KARTI RENDER EDİLİYOR (DEĞİŞTİRİLMEDİ) ---
                            <div className="col-sm-6 col-md-4 col-lg-3" key={item.BrandID}>
                                <Link to={`/collectiondetail?type=brandId&value=${item.BrandID}`} className="text-decoration-none">
                                    {/* Marka Kartı Renk Düzeltmesi: Uyumlu açık gri ton */}
                                    <div 
                                        className="card h-100 border-0 shadow-sm overflow-hidden text-center p-4 text-dark"
                                        style={{ backgroundColor: '#f8f9fa' }} // Bootstrap'in çok açık gri tonu
                                    >
                                        <Building size={48} className="mx-auto mb-3 text-secondary" />
                                        <h5 className="card-title fw-bold text-dark mb-1">{item.BrandName}</h5>
                                        <p className="card-text small opacity-75">{item.Description || "Ürünleri Gör"}</p>
                                    </div>
                                </Link>
                            </div>
                        )
                    ))}
                </div>
            ) : (
                // Ürün Bulunamadı
                <div className="text-center py-5 bg-light rounded-3">
                    <FilterX size={48} className="text-muted mb-3" />
                    <h4 className="text-muted fw-bold">Bu {isWatches ? 'kategoride ürün' : 'marka'} bulunamadı.</h4>
                    <p className="text-muted">Başka koleksiyonlara göz atmaya ne dersin?</p>
                    <Link to="/collections" className="btn btn-outline-dark mt-2 rounded-pill px-4">Tüm Koleksiyonlara Dön</Link>
                </div>
            )}
        </div>
    );
};

export default CollectionDetail;