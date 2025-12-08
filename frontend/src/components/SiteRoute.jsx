import React, { useEffect } from 'react'; 
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { setNavigator } from '../api'; // 👈 Sadece setNavigator import edildi

import Home from './Home'
import Login from './Login'
import Register from './Register'
import Cart from './Cart'
import Favorites from './Favorites' 
import Collections from './Collections'
import CollectionDetail from './CollectionDetail'
import Admin from './Admin'
import ProductDetail from './ProductDetail'
import Checkout from './Checkout'
import About from './About'; 
import Careers from './Careers';
import Contact from './Contact';
import FAQ from './FAQ';

export default function SiteRoute({ handleLogin, user }) {
  
  const navigate = useNavigate(); 
  
  useEffect(() => {
    // navigate hook'unu api.js'e tanıtıyoruz
    setNavigator(navigate);
  }, [navigate]);

  const isAdmin = user?.role === 'admin';

  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route path="/about" element={<About />} />

      <Route path="/careers" element={<Careers />} />

      <Route path="/contact" element={<Contact />} />
       
      <Route path="/faq" element={<FAQ />} />

      <Route path="/login" element={<Login onLogin={handleLogin} />} />

      <Route path="/register" element={<Register />} />

      <Route path="/cart" element={<Cart />} />

      <Route path="/favorites" element={<Favorites />} />

      <Route path="/collections" element={<Collections />} />

      <Route path="/collectiondetail" element={<CollectionDetail />} />

      <Route path="/product/:id" element={<ProductDetail />} />

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