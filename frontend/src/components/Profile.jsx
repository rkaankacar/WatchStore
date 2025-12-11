import React, { useState, useEffect } from "react";
import { ShoppingBag, User, MapPin, KeyRound, RefreshCw, Loader } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../api";

const Profile = ({ user }) => {
    const navigate = useNavigate();

    const [activeTab, setActiveTab] = useState("orders");

    const [userData, setUserData] = useState({
        Email: "",
        Phone: "",
        Address: "",
        City: "",
        Country: "",
    });

    const [passwordData, setPasswordData] = useState({
        currentPassword: "",
        newPassword: "",
        confirmNewPassword: "",
    });

    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [ordersLoading, setOrdersLoading] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState("");
    const [isError, setIsError] = useState(false);

    const USER_ID = user?.UserID || user?.id;

    const ENDPOINTS = {
        USER_INFO: `/api/v1/users/${USER_ID}`,
        USER_UPDATE: `/api/v1/users/update/${USER_ID}`,
        PASSWORD_CHANGE: `/api/v1/users/change-password`,
        // USER_ORDERS: `/api/v1/orders/${USER_ID}`,  // ❌ YORUMA ALINDI
    };

    useEffect(() => {
        if (!USER_ID) {
            setLoading(false);
            setIsError(true);
            setMessage("Kullanıcı ID bulunamadı.");
            return;
        }
        fetchUserData();
    }, [USER_ID]);

    // ❌ Siparişleri çeken useEffect YORUMA ALINDI
    // useEffect(() => {
    //     if (activeTab === "orders" && USER_ID && orders.length === 0) {
    //         fetchOrders();
    //     }
    // }, [activeTab]);

    const fetchUserData = async () => {
        setLoading(true);
        setIsError(false);
        setMessage("");

        try {
            const userRes = await api.get(ENDPOINTS.USER_INFO);

            setUserData({
                Email: userRes.data.email || userRes.data.Email || "",
                Phone: userRes.data.phone || userRes.data.Phone || "",
                Address: userRes.data.address || userRes.data.Address || "",
                City: userRes.data.city || userRes.data.City || "",
                Country: userRes.data.country || userRes.data.Country || "",
            });

        } catch (err) {
            console.error("Kullanıcı bilgisi çekilemedi:", err.response?.data || err);
            setIsError(true);
            setMessage("Kullanıcı bilgileri yüklenemedi.");
        } finally {
            setLoading(false);
        }
    };

    // ❌ Sipariş ÇEKEN FONKSİYON YORUMA ALINDI
    // const fetchOrders = async () => {
    //     setOrdersLoading(true);

    //     try {
    //         const orderRes = await api.get(ENDPOINTS.USER_ORDERS);
    //         setOrders(orderRes.data || []);

    //     } catch (err) {
    //         console.error("Siparişler çekilemedi:", err.response?.data || err);
    //         setOrders([]);
    //     } finally {
    //         setOrdersLoading(false);
    //     }
    // };

    const fetchData = async () => {
        await fetchUserData();
        // ❌ Sipariş fetch YORUMA ALINDI
        // if (activeTab === "orders") {
        //     await fetchOrders();
        // }
    };

    const handleInfoChange = (e) => {
        setUserData((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handlePasswordChange = (e) => {
        setPasswordData((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    };

    const handleInfoSubmit = async (e) => {
        e.preventDefault();

        setSubmitting(true);
        setMessage("");

        try {
            await api.put(ENDPOINTS.USER_UPDATE, userData);
            setMessage("Bilgiler başarıyla güncellendi!");
            setIsError(false);

        } catch (err) {
            console.error("Güncelleme hatası:", err.response?.data || err);
            setIsError(true);
            setMessage(err.response?.data?.detail || "Bilgiler güncellenirken hata oluştu.");
        } finally {
            setSubmitting(false);
        }
    };

    const handlePasswordSubmit = async (e) => {
        e.preventDefault();

        if (passwordData.newPassword !== passwordData.confirmNewPassword) {
            setIsError(true);
            setMessage("Yeni şifreler uyuşmuyor.");
            return;
        }

        if (passwordData.newPassword.length < 6) {
            setIsError(true);
            setMessage("Yeni şifre en az 6 karakter olmalı.");
            return;
        }

        setSubmitting(true);
        setMessage("");

        try {
            await api.put(ENDPOINTS.PASSWORD_CHANGE, {
                current_password: passwordData.currentPassword,
                new_password: passwordData.newPassword,
                new_password_again: passwordData.confirmNewPassword,
            });

            setMessage("Şifre başarıyla değiştirildi!");
            setIsError(false);
            setPasswordData({ currentPassword: "", newPassword: "", confirmNewPassword: "" });

        } catch (err) {
            console.error("Şifre değiştirme hatası:", err.response?.data || err);
            setIsError(true);
            setMessage(err.response?.data?.detail || "Şifre güncellenemedi.");
        } finally {
            setSubmitting(false);
        }
    };

    const handleOrderClick = (id) => {
        navigate(`/siparis/${id}`);
    };

    if (loading)
        return (
            <div className="d-flex justify-content-center align-items-center vh-100">
                <Loader size={32} className="spinner-grow text-dark" />
            </div>
        );

    return (
        <div className="container py-5">

            <div className="d-flex align-items-center justify-content-between mb-4">
                <div className="d-flex align-items-center text-dark">
                    <User size={32} className="me-2" />
                    <h2 className="fw-bold m-0 text-dark">Profilim</h2>
                </div>

                <button className="btn btn-outline-dark btn-sm rounded-pill px-3" onClick={fetchData}>
                    <RefreshCw size={16} className="me-1" /> Yenile
                </button>
            </div>

            <div className="row">
                <div className="col-md-3 mb-4">
                    <div className="list-group shadow-sm border-0">

                        <button
                            className={`list-group-item list-group-item-action py-3 ${activeTab === "orders" ? "active bg-dark text-white fw-bold" : ""
                                }`}
                            onClick={() => setActiveTab("orders")}
                        >
                            <ShoppingBag size={18} className="me-2" /> Siparişlerim
                        </button>

                        <button
                            className={`list-group-item list-group-item-action py-3 ${activeTab === "info" ? "active bg-dark text-white fw-bold" : ""
                                }`}
                            onClick={() => setActiveTab("info")}
                        >
                            <User size={18} className="me-2" /> Bilgilerim
                        </button>

                    </div>
                </div>

                <div className="col-md-9">

                    {message && (
                        <div className={`alert ${isError ? "alert-danger" : "alert-success"}`}>{message}</div>
                    )}

                    {/* ❌ Siparişlerim kısmı komple yorumda */}
                    {/*
                    {activeTab === "orders" && (
                        <div className="card border-0 shadow-sm">
                            <div className="card-header bg-white py-3 border-bottom-0">
                                <h5 className="m-0 fw-bold">Siparişlerim ({orders.length})</h5>
                            </div>

                            {ordersLoading ? (
                                <div className="text-center py-5">
                                    <Loader size={32} className="spinner-border text-dark" />
                                    <p className="mt-3 text-muted">Siparişler yükleniyor...</p>
                                </div>
                            ) : (
                                <div className="table-responsive">
                                    <table className="table table-hover">
                                        <thead className="table-light">
                                            <tr>
                                                <th className="ps-4">No</th>
                                                <th>Tarih</th>
                                                <th>Tutar</th>
                                                <th>Durum</th>
                                                <th className="text-end pe-4">Detay</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {orders.length ? (
                                                orders.map((order) => (
                                                    <tr
                                                        key={order.OrderID}
                                                        onClick={() => handleOrderClick(order.OrderID)}
                                                        style={{ cursor: "pointer" }}
                                                    >
                                                        <td className="ps-4 fw-bold">#{order.OrderID}</td>
                                                        <td>{new Date(order.OrderDate).toLocaleDateString()}</td>
                                                        <td>₺{parseFloat(order.TotalAmount).toLocaleString()}</td>
                                                        <td>
                                                            <span className="badge bg-warning text-dark">
                                                                {order.Status}
                                                            </span>
                                                        </td>
                                                        <td className="text-end pe-4">
                                                            <button className="btn btn-sm btn-outline-dark">
                                                                Detay
                                                            </button>
                                                        </td>
                                                    </tr>
                                                ))
                                            ) : (
                                                <tr>
                                                    <td colSpan="5" className="text-center py-5 text-muted">
                                                        <ShoppingBag size={48} className="mb-3 opacity-25" />
                                                        <p className="mb-0">Henüz hiç sipariş vermediniz.</p>
                                                    </td>
                                                </tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    )}
                    */}

                    {/* BİLGİLER */}
                    {activeTab === "info" && (
                        <>
                            <div className="card p-4 shadow-sm border-0 mb-4">
                                <h4 className="fw-bold mb-4 border-bottom pb-2">
                                    <MapPin className="me-2" /> Bilgilerim
                                </h4>

                                <form onSubmit={handleInfoSubmit} className="row g-3">
                                    <div className="col-md-6">
                                        <label className="form-label">Email</label>
                                        <input
                                            type="email"
                                            name="Email"
                                            value={userData.Email}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>

                                    <div className="col-md-6">
                                        <label className="form-label">Telefon</label>
                                        <input
                                            type="tel"
                                            name="Phone"
                                            value={userData.Phone}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                        />
                                    </div>

                                    <div className="col-12">
                                        <label className="form-label">Adres</label>
                                        <textarea
                                            name="Address"
                                            value={userData.Address}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                            rows="3"
                                        ></textarea>
                                    </div>

                                    <div className="col-md-6">
                                        <label className="form-label">Şehir</label>
                                        <input
                                            type="text"
                                            name="City"
                                            value={userData.City}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                        />
                                    </div>

                                    <div className="col-md-6">
                                        <label className="form-label">Ülke</label>
                                        <input
                                            type="text"
                                            name="Country"
                                            value={userData.Country}
                                            onChange={handleInfoChange}
                                            className="form-control bg-light border-0"
                                        />
                                    </div>

                                    <div className="col-12 text-end">
                                        <button className="btn btn-dark px-4" disabled={submitting}>
                                            {submitting ? "Güncelleniyor..." : "Güncelle"}
                                        </button>
                                    </div>
                                </form>
                            </div>

                            <div className="card p-4 shadow-sm border-0">
                                <h4 className="fw-bold mb-4 border-bottom pb-2">
                                    <KeyRound className="me-2" /> Şifre Değiştir
                                </h4>

                                <form onSubmit={handlePasswordSubmit} className="row g-3">
                                    <div className="col-md-12">
                                        <label className="form-label">Mevcut Şifre</label>
                                        <input
                                            type="password"
                                            name="currentPassword"
                                            value={passwordData.currentPassword}
                                            onChange={handlePasswordChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>

                                    <div className="col-md-6">
                                        <label className="form-label">Yeni Şifre</label>
                                        <input
                                            type="password"
                                            name="newPassword"
                                            value={passwordData.newPassword}
                                            onChange={handlePasswordChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>

                                    <div className="col-md-6">
                                        <label className="form-label">Yeni Şifre (Tekrar)</label>
                                        <input
                                            type="password"
                                            name="confirmNewPassword"
                                            value={passwordData.confirmNewPassword}
                                            onChange={handlePasswordChange}
                                            className="form-control bg-light border-0"
                                            required
                                        />
                                    </div>

                                    <div className="col-12 text-end">
                                        <button className="btn btn-warning px-4" disabled={submitting}>
                                            {submitting ? "Değiştiriliyor..." : "Şifreyi Değiştir"}
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Profile;
