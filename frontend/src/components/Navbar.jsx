import React, { useState } from 'react';
import { ShoppingCart, User, Menu, X, Watch, LogOut, UserPlus, LogIn, LayoutDashboard, Heart, Search } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = ({ user, handleLogout }) => {
  const [isNavOpen, setIsNavOpen] = useState(false);
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchTerm)}`);
      setIsNavOpen(false);
      setSearchTerm('');
    }
  };

  const isAdmin = user?.role === 'admin';

  const onLogoutClick = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_id');
    handleLogout();
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark py-3 sticky-top shadow-sm">
      <div className="container">
        {/* LOGO */}
        <Link className="navbar-brand d-flex align-items-center fw-bold fs-4" to="/">
          <Watch className="me-2 text-warning" /> WatchStore
        </Link>

        {/* MOBİL MENÜ BUTONU */}
        <button
          className="navbar-toggler border-0"
          type="button"
          onClick={() => setIsNavOpen(!isNavOpen)}
        >
          {isNavOpen ? <X size={28} /> : <Menu size={28} />}
        </button>

        {/* MENÜ İÇERİĞİ */}
        <div className={`collapse navbar-collapse ${isNavOpen ? 'show' : ''}`}>
          <ul className="navbar-nav me-auto mb-2 mb-lg-0 mx-auto">
            <li className="nav-item"><Link className="nav-link px-3" to="/">Anasayfa</Link></li>
            <li className="nav-item"><Link className="nav-link px-3" to="/collections">Koleksiyon</Link></li>

            {/* Admin Linki */}
            {isAdmin && (
              <li className="nav-item">
                <Link className="nav-link px-3 text-warning fw-bold" to="/admin">
                  <LayoutDashboard size={18} className="me-1 mb-1" /> Admin Panel
                </Link>
              </li>
            )}
          </ul>

          {/* SEARCH BAR */}
          <form className="d-flex mx-3" onSubmit={handleSearch} role="search">
            <div className="input-group">
              <input
                className="form-control form-control-sm bg-dark text-warning border-secondary"
                type="search"
                placeholder="Marka veya model ara..."
                aria-label="Search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <button className="btn btn-sm btn-outline-warning" type="submit">
                <Search size={16} />
              </button>
            </div>
          </form>

          <div className="d-flex align-items-center gap-3">
            {user ? (
              // --- GİRİŞ YAPMIŞ KULLANICI ---
              <>
                {/* 1. FAVORİLER İKONU */}
                <div className="position-relative">
                  <Link to="/favorites" className="text-white" title="Favorilerim">
                    <Heart className="cursor-pointer hover-scale" size={24} />
                  </Link>
                </div>

                {/* 2. SEPET İKONU */}
                <div className="position-relative">
                  <Link to="/cart" className="text-white" title="Sepetim">
                    <ShoppingCart className="cursor-pointer hover-scale" size={24} />
                  </Link>
                </div>

                {/* 3. PROFİL VE ÇIKIŞ (DEĞİŞİKLİK BURADA YAPILDI) */}

                {/* Kullanıcı Adı Linki */}
                <Link to="/profil" className="text-decoration-none text-white" title="Profilim">
                  <div className="d-flex align-items-center gap-2 border-start ps-3 ms-2 border-secondary">
                    <span className="text-white small d-none d-md-block">
                      {user.name}
                    </span>
                  </div>
                </Link>

                {/* Çıkış Butonu */}
                <button
                  className="btn btn-sm btn-outline-danger d-flex align-items-center gap-2 rounded-pill px-3 ms-2"
                  onClick={onLogoutClick}
                  title="Çıkış Yap"
                >
                  <LogOut size={16} />
                </button>
              </>
            ) : (
              // --- MİSAFİR KULLANICI ---
              <div className="d-flex gap-2">
                <Link to="/login" className="btn btn-sm btn-outline-light rounded-pill px-3 d-flex align-items-center gap-1">
                  <LogIn size={16} /> Giriş
                </Link>
                <Link to="/register" className="btn btn-sm btn-warning rounded-pill px-3 d-flex align-items-center gap-1 text-dark fw-bold">
                  <UserPlus size={16} /> Kayıt Ol
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;