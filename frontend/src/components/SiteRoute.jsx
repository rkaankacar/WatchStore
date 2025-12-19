import React, { useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { setNavigator } from '../services/api';

import Home from '../pages/Home'
import Login from '../pages/Login'
import Register from '../pages/Register'
import Cart from '../pages/Cart'
import Favorites from '../pages/Favorites'
import Collections from '../pages/Collections'
import CollectionDetail from '../pages/CollectionDetail'
import Admin from '../pages/Admin'
import ProductDetail from '../pages/ProductDetail'
import Checkout from '../pages/Checkout'
import About from '../pages/About';
import Careers from '../pages/Careers';
import Contact from '../pages/Contact';
import FAQ from '../pages/FAQ';
import Profile from '../pages/Profile';// <-- Profile bileşeninizi buraya eklediğinizden emin olun
import ReturnDetails from '../pages/ReturnDetails';
import SearchResults from '../pages/SearchResults';


export default function SiteRoute({ handleLogin, user }) {

      const navigate = useNavigate();

      useEffect(() => {
            // navigate hook'unu api.js'e tanıtıyoruz
            setNavigator(navigate);
      }, [navigate]);

      const isAuthenticated = !!user; // Kullanıcının giriş yapıp yapmadığını kontrol eder
      const isAdmin = user?.role === 'admin';

      return (
            <Routes>
                  <Route path="/" element={<Home />} />

                  <Route path="/about" element={<About />} />
                  <Route path="/careers" element={<Careers />} />
                  <Route path="/contact" element={<Contact />} />
                  <Route path="/faq" element={<FAQ />} />
                  <Route path="/return-details" element={<ReturnDetails />} />
                  <Route path="/login" element={<Login onLogin={handleLogin} />} />
                  <Route path="/register" element={<Register />} />

                  <Route path="/cart" element={<Cart />} />
                  <Route path="/favorites" element={<Favorites />} />

                  <Route path="/collections" element={<Collections />} />
                  <Route path="/collectiondetail" element={<CollectionDetail />} />
                  <Route path="/product/:id" element={<ProductDetail />} />
                  <Route path="/checkout" element={<Checkout user={user} />} />
                  <Route path="/search" element={<SearchResults />} />


                  {/* 1. PROFİL KORUMASI */}
                  <Route
                        path="/profil"
                        element={
                              isAuthenticated ? (
                                    <Profile user={user} /> // user prop'unu Profile bileşenine aktarıyoruz
                              ) : (
                                    <Navigate to="/login" replace /> // Giriş yapmamışsa Login sayfasına yönlendir
                              )
                        }
                  />



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

                  {/* 404 (Eşleşmeyen tüm yollar için) */}
                  <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
      )
}
