import { Routes, Route, Navigate } from 'react-router-dom'
import Home from './Home'
import Login from './Login'
import Register from './Register'
import Cart from './Cart'
import Favorites from './Favorites' // <--- 1. IMPORT EKLENDİ
import Collections from './Collections'
import CollectionDetail from './CollectionDetail'
import Admin from './Admin'
import ProductDetail from './ProductDetail'
// Checkout dosyan henüz hazır değilse bu satırı yoruma alabilirsin
import Checkout from './Checkout'

export default function SiteRoute({ handleLogin, user }) {

  // ESKİ: const isAdmin = user?.email === 'admin@watchstore.com';
  // YENİ: Backend'den gelen role bilgisine bakıyoruz
  const isAdmin = user?.role === 'admin';

  return (
    <Routes>
      {/* ARTIK PROPS YOK! 
          Home, ProductDetail, Admin... Hepsi kendi verisini kendi çekiyor.
      */}

      <Route path="/" element={<Home />} />

      {/* Login başarılı olunca App.js'teki state'i güncellemek için handleLogin lazım */}
      <Route path="/login" element={<Login onLogin={handleLogin} />} />

      {/* Register artık login yapmıyor, sadece kaydedip yönlendiriyor */}
      <Route path="/register" element={<Register />} />

      <Route path="/cart" element={<Cart />} />

      {/* 2. ROUTE EKLENDİ: Favoriler Sayfası */}
      <Route path="/favorites" element={<Favorites />} />

      <Route path="/collections" element={<Collections />} />

      {/* Dinamik Kategori Sayfası (Men, Women vb.) */}
      <Route path="/collectiondetail" element={<CollectionDetail />} />

      {/* Dinamik Ürün Detayı (ID ile) */}
      <Route path="/product/:id" element={<ProductDetail />} />

      {/* Ödeme Sayfası (Dosya varsa çalışır) */}
      <Route path="/checkout" element={<Checkout />} />

      {/* ADMIN KORUMASI */}
      <Route
        path="/admin"
        element={
          isAdmin ? (
            <Admin />
          ) : (
            <Navigate to="/" replace />
          )
        }
      />
    </Routes>
  )
}