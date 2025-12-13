import React, { useEffect, useState } from "react";
import api from "../api";

export default function ReturnDetails() {
  const [returns, setReturns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReturns = async () => {
      try {
        // Backend'deki get_multi_by_user metoduna hitap eden endpoint
        const res = await api.get("/api/v1/returns/my-requests");
        setReturns(res.data);
      } catch (err) {
        console.error("İade talepleri alınamadı:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchReturns();
  }, []);

  const statusBadge = (status) => {
    // Backend'de status alanını küçük harfle ('pending', 'approved') tutuyorsanız,
    // buradaki case'leri de küçük harfe çevirmeniz gerekebilir.
    switch (status) {
      case "Beklemede":
        return <span className="badge bg-warning text-dark">Beklemede</span>;
      case "Onaylandı": // Eğer onaylandı olarak geliyorsa
      case "Tamamlandı": // Eğer tamamlandı olarak geliyorsa
        return <span className="badge bg-success">Onaylandı</span>;
      case "Reddedildi":
        return <span className="badge bg-danger">Reddedildi</span>;
      default:
        return <span className="badge bg-secondary">{status}</span>;
    }
  };
  
  // Ürün adlarını ve miktarlarını döngüleyerek listeleyen yardımcı fonksiyon
  const renderProductDetails = (order) => {
    if (!order || !order.order_details || order.order_details.length === 0) {
      return <p className="mb-1"><strong>Ürün:</strong> Bilgi Bulunamadı</p>;
    }

    // Siparişteki tüm ürünleri listeliyoruz
    return order.order_details.map((detail, index) => (
      <p key={index} className="mb-1">
        <strong>Ürün {order.order_details.length > 1 ? index + 1 : ''}:</strong> 
        {/*
          ZİNCİR: item.order.order_details[index].watch.brand.BrandName + item.order.order_details[index].watch.ModelName
          Alan adlarını Pydantic şemanıza göre kontrol edin (BrandName, ModelName, vs.)
        */}
        {detail.watch?.brand?.BrandName} {detail.watch?.ModelName} 
        {detail.quantity > 1 && ` (x${detail.quantity})`}
      </p>
    ));
  };


  return (
    <div className="container my-5" style={{ minHeight: "50vh" }}>
      <h2 className="text-center mb-4">📦 İade Taleplerim</h2>

      {loading && <p className="text-center">Yükleniyor...</p>}

      {!loading && returns.length === 0 && (
        <p className="text-center text-muted">
          Henüz oluşturulmuş bir iade talebiniz yok.
        </p>
      )}

      {!loading &&
        returns.map((item) => (
          <div key={item.id} className="card mb-3 shadow-sm">
            <div className="card-body">
              <div className="d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">
                  Sipariş No: <strong>{item.OrderID}</strong> {/* Pydantic'ten gelen 'order_id' kullanıldı */}
                </h5>
                {statusBadge(item.Status)} {/* Pydantic'ten gelen 'status' kullanıldı */}
              </div>

              <hr />

              {/* Ürün Adı Listesi */}
              {renderProductDetails(item.order)}

              <p className="mb-1">
                <strong>İade Sebebi:</strong> {item.Reason} {/* Pydantic'ten gelen 'reason' kullanıldı */}
              </p>
              
              {/* Açıklama alanı (description) isteğe bağlı olduğu için kontrol ederek gösterelim */}
              {item.Description && (
                  <p className="mb-1">
                    <strong>Açıklama:</strong> {item.Description}
                  </p>
              )}

              <p className="mb-1">
                <strong>Talep Tarihi:</strong>{" "}
                {new Date(item.CreatedAt).toLocaleDateString("tr-TR")} {/* Pydantic'ten gelen 'created_at' kullanıldı */}
              </p>

              {/* Müşteri görünümünde admin notu gösterilmez, bu kısım çıkarıldı. */}
            </div>
          </div>
        ))}
    </div>
  );
}