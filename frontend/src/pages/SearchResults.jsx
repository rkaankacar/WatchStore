import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { Watch, ShoppingBag, ArrowLeft, FilterX, Search } from 'lucide-react';
import api from "../services/api";
import { getErrorMessage } from "../utils/error";

const SearchResults = () => {
    const [searchParams] = useSearchParams();
    const query = searchParams.get('q');

    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchSearchResults = async () => {
            if (!query) return;

            setLoading(true);
            try {
                // Backend'deki arama endpoint'ine istek at
                const response = await api.get(`/api/v1/watches/?q=${encodeURIComponent(query)}`);
                setData(response.data);
            } catch (err) {
                console.error("Arama sonuçları yüklenemedi:", getErrorMessage(err));
                setData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchSearchResults();
    }, [query]);

    if (loading) return (
        <div className="d-flex justify-content-center align-items-center py-5" style={{ minHeight: '50vh' }}>
            <div className="spinner-border text-dark" role="status">
                <span className="visually-hidden">Aranıyor...</span>
            </div>
        </div>
    );

    return (
        <div className="container py-5">
            {/* Üst Başlık */}
            <div className="mb-5 border-bottom pb-3">
                <Link to="/" className="text-decoration-none text-muted d-inline-flex align-items-center mb-2 hover-dark">
                    <ArrowLeft size={18} className="me-2" /> Anasayfaya Dön
                </Link>
                <div className="d-flex justify-content-between align-items-end">
                    <div>
                        <h2 className="fw-bold display-6 mb-0">
                            "{query}" için Arama Sonuçları
                        </h2>
                        <p className="text-muted mb-0 mt-2 small">Topam {data.length} sonuç bulundu.</p>
                    </div>
                </div>
            </div>

            {data.length > 0 ? (
                <div className="row g-4">
                    {data.map((item) => (
                        <div className="col-sm-6 col-md-4 col-lg-3" key={item.WatchID}>
                            <Link to={`/product/${item.WatchID}`} className="text-decoration-none">
                                <div className="card h-100 border-0 shadow-sm overflow-hidden product-card" style={{ transition: 'transform 0.2s' }}>
                                    <div className="position-relative bg-light d-flex align-items-center justify-content-center p-4" style={{ height: '260px' }}>
                                        {item.ImageUrl ? (
                                            <img
                                                src={item.ImageUrl}
                                                alt={item.ModelName}
                                                style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', mixBlendMode: 'multiply' }}
                                            />
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
                                        <p className="text-dark fw-bold mb-1 text-uppercase small">
                                            {item.brand?.BrandName || item.Brand?.BrandName || "MARKA BİLİNMİYOR"}
                                        </p>

                                        <h6 className="card-title fw-bold text-dark text-truncate" title={item.ModelName}>
                                            {item.ModelName}
                                        </h6>

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
                    ))}
                </div>
            ) : (
                // Sonuç Bulunamadı
                <div className="text-center py-5 bg-light rounded-3">
                    <Search size={48} className="text-muted mb-3" />
                    <h4 className="text-muted fw-bold">"{query}" ile eşleşen ürün bulunamadı.</h4>
                    <p className="text-muted">Lütfen farklı anahtar kelimelerle tekrar deneyin veya koleksiyonlarımıza göz atın.</p>
                    <Link to="/collections" className="btn btn-outline-dark mt-2 rounded-pill px-4">Koleksiyonları Keşfet</Link>
                </div>
            )}
        </div>
    );
};

export default SearchResults;
