import React from 'react';
import { Watch, Instagram, Twitter, Facebook } from 'lucide-react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark text-light py-5 mt-auto">
      <div className="container">
        <div className="row g-4">
          {/* Logo ve Açıklama */}
          <div className="col-md-4">
            <div className="d-flex align-items-center mb-3">
              <Watch className="text-warning me-2" size={24} />
              <h5 className="m-0 fw-bold">WatchStore</h5>
            </div>
            <p className="text-white small">
              Zamanın ötesinde tasarımlarla tarzınızı yansıtın.
              En kaliteli saat koleksiyonları burada.
            </p>
          </div>

          {/* Linkler - React Router Link kullandık */}
          <div className="col-md-2 col-6">
            <h6 className="fw-bold mb-3 text-warning">Kurumsal</h6>
            <ul className="list-unstyled small text-muted">
              <li className="mb-2"><Link to="/about" className="text-decoration-none text-white">Hakkımızda</Link></li>
              <li className="mb-2"><Link to="/careers" className="text-decoration-none text-white">Kariyer</Link></li>
              <li className="mb-2"><Link to="/contact" className="text-decoration-none text-white">İletişim</Link></li>
            </ul>
          </div>

          <div className="col-md-2 col-6">
            <h6 className="fw-bold mb-3 text-warning">Yardım</h6>
            <ul className="list-unstyled small text-muted">
              <li className="mb-2"><Link to="/" className="text-decoration-none text-white">Sipariş Takibi</Link></li>
              <li className="mb-2"><Link to="/" className="text-decoration-none text-white">İade & Değişim</Link></li>
              <li className="mb-2"><Link to="/faq" className="text-decoration-none text-white">S.S.S.</Link></li>
            </ul>
          </div>

          {/* Sosyal Medya - Dış link olduğu için <a> kalabilir */}
          <div className="col-md-4">
            <h6 className="fw-bold mb-3 text-warning">Bizi Takip Edin</h6>
            <div className="d-flex gap-3">
              <a href="https://instagram.com" target="_blank" rel="noreferrer" className="text-light hover-scale"><Instagram size={20} /></a>
              <a href="https://twitter.com" target="_blank" rel="noreferrer" className="text-light hover-scale"><Twitter size={20} /></a>
              <a href="https://facebook.com" target="_blank" rel="noreferrer" className="text-light hover-scale"><Facebook size={20} /></a>
            </div>
          </div>
        </div>

        <hr className="border-secondary my-4" />

        {/* Dinamik Tarih */}
        <div className="text-center text-white small">
          &copy; {currentYear} WatchStore. Tüm hakları saklıdır.
        </div>
      </div>
    </footer>
  );
};

export default Footer;