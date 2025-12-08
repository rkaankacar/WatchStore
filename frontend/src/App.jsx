import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';       // Dosyaların yeri doğru mu? (src içindeyse ./Navbar yap)
import SiteRoute from './components/SiteRoute'; // Dosyaların yeri doğru mu? (src içindeyse ./SiteRoute yap)
import Footer from './components/Footer';       // Footer dosyan var mı? Yoksa bu satırı sil.

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('token');
      const role = localStorage.getItem('user_role');
      const id = localStorage.getItem('user_id');
      // Login.jsx içinde 'user_name' diye kaydetmediysen burası null gelir.
      // İstersen Login.jsx'te localStorage.setItem('user_name', ...) ekle.
      const name = localStorage.getItem('user_name');

      if (token) {
        setUser({
          id: id,
          role: role,
          name: name || "Kullanıcı"
        });
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
  };

  if (loading) return <div className="text-center mt-5">Yükleniyor...</div>;

  return (


    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar user={user} handleLogout={handleLogout} />

      <div className="flex-grow-1">
        <SiteRoute
          handleLogin={handleLogin}
          user={user}
        />
      </div>

      {/* Footer dosyan yoksa bu satırı sil veya yorum satırı yap */}
      {Footer && <Footer />}
    </div>

  );
}

export default App;