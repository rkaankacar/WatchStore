import React, { useState, useEffect } from 'react';
import { Watch, ArrowRight, Star, Loader } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../api';

const Home = () => {
    const [watches, setWatches] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchWatches = async () => {
            try {
                const response = await api.get('/api/v1/watches/');
                setWatches(response.data);
            } catch (err) {
                console.error("Ürünler çekilemedi:", err);
            } finally {
                setLoading(false);
            }
        };

        fetchWatches();
    }, []);

    // İlk 3 ürünü al, yoksa boş dizi döndür (Hata önleyici)
    const featuredProducts = Array.isArray(watches) ? watches.slice(0, 3) : [];

    if (loading) return (
        <div className="d-flex justify-content-center align-items-center vh-100">
            <div className="spinner-border text-dark" role="status">
                <span className="visually-hidden">Yükleniyor...</span>
            </div>
        </div>
    );

    return (
        <div>
            {/* --- HERO (Banner) BÖLÜMÜ --- */}
            <header className="py-5 text-center text-white" style={{ background: 'linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%)' }}>
                <div className="container py-5">
                    <div className="row justify-content-center">
                        <div className="col-lg-8">
                            <h1 className="display-3 fw-bold mb-3 animate__animated animate__fadeInDown">Zamanı Yönet</h1>
                            <p className="lead text-white-50 mb-4 px-5">
                                Dünyanın en prestijli saat markaları, eşsiz tasarımlar ve <br className="d-none d-md-block" />
                                kusursuz mekanizmalar şimdi bileğinizde.
                            </p>
                            <Link to="/collections" className="btn btn-warning btn-lg px-5 fw-bold rounded-pill shadow-lg hover-scale">
                                Keşfetmeye Başla <ArrowRight size={20} className="ms-2" />
                            </Link>
                        </div>
                    </div>
                </div>
            </header>

            {/* --- ÖNE ÇIKAN ÜRÜNLER --- */}
            <section className="container py-5">
                <div className="text-center mb-5">
                    <h2 className="fw-bold display-6">Öne Çıkan Modeller</h2>
                    <p className="text-muted">Bu haftanın en çok tercih edilenleri</p>
                </div>

                {featuredProducts.length === 0 ? (
                    <div className="text-center py-5 bg-light rounded-3">
                        <Watch size={48} className="text-muted mb-3 opacity-50" />
                        <h5 className="text-muted">Koleksiyonlar hazırlanıyor...</h5>
                    </div>
                ) : (
                    <div className="row g-4">
                        {featuredProducts.map((product) => (
                            <div className="col-md-4" key={product.WatchID}>

                                <Link to={`/product/${product.WatchID}`} className="text-decoration-none">
                                    <div className="card h-100 border-0 shadow-lg overflow-hidden hover-scale product-card">

                                        {/* RESİM ALANI */}
                                        <div className="card-img-top d-flex align-items-center justify-content-center bg-white p-4" style={{ height: '280px' }}>
                                            {product.ImageUrl ? (
                                                <img
                                                    src={product.ImageUrl}
                                                    alt={product.ModelName}
                                                    style={{ maxHeight: '100%', maxWidth: '100%', objectFit: 'contain', transition: 'transform 0.3s' }}
                                                    className="img-fluid"
                                                />
                                            ) : (
                                                <Watch size={80} strokeWidth={1} className="text-secondary opacity-25" />
                                            )}
                                        </div>

                                        <div className="card-body text-center p-4 bg-white">
                                        
                                            {/* 🔥 GÜNCELLENEN KISIM: Marka Adı eklendi */}
                                            <p className="text-dark fw-bold mb-1 text-uppercase small">
                                                {product.brand?.BrandName || product.Brand?.BrandName || "MARKA BİLİNMİYOR"}
                                            </p>

                                            <h5 className="card-title fw-bold mb-2 text-dark text-truncate">{product.ModelName}</h5>

                                            <p className="text-dark fs-4 fw-bold mb-3">
                                                ₺{parseFloat(product.Price).toLocaleString()}
                                            </p>

                                            <button className="btn btn-outline-dark w-100 rounded-pill fw-bold btn-sm py-2">
                                                Detayları Gör
                                            </button>
                                        </div>
                                    </div>
                                </Link>
                            </div>
                        ))}
                    </div>
                )}
            </section>
        </div>
    );
};

export default Home;