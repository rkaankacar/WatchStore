import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import SiteRoute from './components/SiteRoute';
import Footer from './components/Footer';
import { setLogoutHandler } from './api'; // logout handler ekledik

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = () => {
      const token = localStorage.getItem('token');
      const role = localStorage.getItem('user_role');
      const id = localStorage.getItem('user_id');
      const name = localStorage.getItem('user_name');

      if (token) {
        setUser({ id, role, name: name || "Kullanıcı" });
      }
      setLoading(false);
    };

    checkAuth();

    // API logout olayı geldiğinde user state sıfırlansın
    setLogoutHandler(() => {
      setUser(null);
    });
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
    localStorage.removeItem('user_id');
    localStorage.removeItem('user_name');
  };

  if (loading) return <div className="text-center mt-5">Yükleniyor...</div>;

  return (
    <div className="d-flex flex-column min-vh-100 bg-light">
      <Navbar user={user} handleLogout={handleLogout} />
      <div className="flex-grow-1">
        <SiteRoute handleLogin={handleLogin} user={user} />
      </div>
      {Footer && <Footer />}
    </div>
  );
}

export default App;
