import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

// Statik Kategori Verisi
const categories = [
  {
    id: 'erkek',
    name: 'Erkek Saatleri',
    description: 'Maskülen çizgiler ve güçlü tasarımlar.',
    // Yönlendirme: CollectionDetails sayfasına gender filtresiyle git
    link: '/collectiondetail?type=gender&value=Erkek',
    style: { backgroundColor: '#212529', color: 'white' }
  },
  {
    id: 'kadin',
    name: 'Kadın Saatleri',
    description: 'Zarafet ve şıklığı buluşturan özel tasarımlar.',
    // Yönlendirme: CollectionDetails sayfasına gender filtresiyle git
    link: '/collectiondetail?type=gender&value=Kadın',
    style: { backgroundColor: '#ffc107', color: '#212529' }
  },
  {
    id: 'cocuk',
    name: 'Çocuk Saatleri',
    description: 'Çocuklarımız için zamansız modeller.',
    // Yönlendirme: CollectionDetails sayfasına gender filtresiyle git
    link: '/collectiondetail?type=gender&value=Çocuk',
    style: { backgroundColor: '#6c757d', color: 'white' }
  },
  {
    id: 'markalar',
    name: 'Tüm Markalar',
    description: 'En sevilen markaların tüm koleksiyonlarını keşfet.',
    // 🎯 KRİTİK DÜZELTME: Artık '/brands' yerine tek dinamik rotayı kullanıyor
    link: '/collectiondetail?type=brands',
    style: { backgroundColor: '#a6d4fa', color: '#212529' }
  },
];

const Collections = () => {

  return (
    <div className="container py-5">
      <h2 className="text-center fw-bold mb-5">Koleksiyonlarımızı Keşfedin</h2>

      <div className="row g-4">
        {categories.map((category) => (
          <div key={category.id} className="col-md-6">
            <div className="card h-100 border-0 shadow-sm" style={category.style}>
              <div
                className="card-body p-5 d-flex flex-column justify-content-center align-items-start"
                style={{ minHeight: '250px' }}
              >
                <h3 className="fw-bold mb-2">{category.name}</h3>

                <p className="mb-4 opacity-75">
                  {category.description}
                </p>

                <Link
                  to={category.link}
                  // Link butonunun stilini arka plana göre ayarla
                  className={`btn ${category.style.color === 'white' ? 'btn-light' : 'btn-dark'} rounded-pill px-4 fw-bold shadow-sm d-flex align-items-center`}
                >
                  İncele <ArrowRight size={18} className="ms-2" />
                </Link>

              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Collections;