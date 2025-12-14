# Saat Satış E-Ticaret Platformu 🕐

Modern ve kullanıcı dostu bir saat satış e-ticaret platformu. FastAPI backend ve React frontend ile geliştirilmiş tam özellikli bir online mağaza sistemi.

## 🌟 Özellikler

### 👤 Kullanıcı Özellikleri
- **Kullanıcı Kaydı ve Girişi**: JWT tabanlı güvenli kimlik doğrulama
- **Profil Yönetimi**: Kişisel bilgiler ve şifre güncelleme
- **Favoriler**: Ürünleri favorilere ekleme ve yönetme
- **Sepet Yönetimi**: Alışveriş sepeti işlemleri
- **Sipariş Geçmişi**: Geçmiş siparişleri görüntüleme ve takip
- **İade Talepleri**: Sipariş iade süreci yönetimi
- **Ürün Yorumları**: Ürünler için puanlama ve yorum yapma

### 🛒 Alışveriş Özellikleri
- **Ürün Kataloğu**: Markalara göre filtrelenmiş saat koleksiyonu
- **Detaylı Ürün Sayfaları**: Yüksek kaliteli görseller ve teknik özellikler
- **Stok Yönetimi**: Gerçek zamanlı stok kontrolü
- **Gelişmiş Arama**: Ürün adı ve markaya göre arama
- **Sepet İşlemleri**: Ürün ekleme, çıkarma, miktar güncelleme

### 💳 Ödeme ve Sipariş
- **Iyzico Entegrasyonu**: Güvenli ödeme sistemi
- **Sipariş Takibi**: Sipariş durumları ve geçmiş
- **E-posta Bildirimleri**: Sipariş onayları ve güncellemeler
- **Fatura Oluşturma**: Otomatik HTML fatura gönderimi

### 👨‍💼 Yönetici Paneli
- **Ürün Yönetimi**: Saat ekleme, düzenleme, silme
- **Marka Yönetimi**: Marka bilgilerini yönetme
- **Sipariş Yönetimi**: Tüm siparişleri görüntüleme ve durum güncelleme
- **Kullanıcı Yönetimi**: Kullanıcı hesaplarını yönetme
- **İade İşlemleri**: İade taleplerini onaylama/reddetme

## 🛠️ Teknoloji Altyapısı

### Backend
- **FastAPI**: Yüksek performanslı asenkron web framework
- **PostgreSQL**: Güçlü ve ölçeklenebilir veritabanı
- **SQLAlchemy**: ORM ile veritabanı işlemleri
- **JWT**: Güvenli token tabanlı kimlik doğrulama
- **Celery**: Arka plan görevleri (e-posta gönderimi)
- **Redis**: Görev kuyruğu için
- **Aiosmtplib**: E-posta gönderimi
- **Iyzico**: Ödeme entegrasyonu

### Frontend
- **React 19**: Modern JavaScript kütüphanesi
- **Vite**: Hızlı geliştirme sunucusu ve build tool
- **React Router**: Sayfa yönlendirme
- **Bootstrap 5**: Responsive tasarım
- **Axios**: HTTP istekleri
- **Lucide React**: İkon kütüphanesi

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis (e-posta görevleri için)
- Ngrok (İyzico için)
- Docker (Redis için)

### Backend Kurulumu

1. **Sanal ortam oluşturun:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Veritabanını hazırlayın:**
```bash
python create_db_schema.py
```

4. **Ortam değişkenlerini ayarlayın (.env dosyası):**
```env
ASYNC_DATABASE_URL=postgresql+asyncpg://kullanici:sifre@localhost:5432/veritabani
SECRET_KEY=guvenli_jwt_anahtari
REDIS_URL=redis://localhost:6379/0
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=sizin_email@gmail.com
SENDER_PASSWORD=email_sifresi
```

5. **Sunucuyu başlatın:**
```bash
uvicorn backend.main:app --reload
```

### Frontend Kurulumu

1. **Bağımlılıkları yükleyin:**
```bash
cd frontend
npm install
```

2. **Geliştirme sunucusunu başlatın:**
```bash
npm run dev
```

## 📁 Proje Yapısı

```
saati-satis-yeni/
├── backend/
│   ├── api/v1/          # API endpoint'leri
│   ├── core/            # Yapılandırma ve güvenlik
│   ├── crud/            # Veritabanı işlemleri
│   ├── database/        # Veritabanı bağlantısı
│   ├── models/          # SQLAlchemy modelleri
│   ├── routers/         # Ek router'lar
│   ├── schemas/         # Pydantic şemaları
│   ├── static/          # Statik dosyalar
│   ├── tests/           # Test dosyaları
│   └── worker/          # Celery görevleri
├── frontend/
│   ├── public/          # Statik varlıklar
│   ├── src/
│   │   ├── components/  # React bileşenleri
│   │   ├── api.js       # API yapılandırması
│   │   └── assets/      # Görseller ve stiller
│   └── package.json
├── .gitignore
└── README.md
```

## 🔧 API Dokümantasyonu

Backend sunucusu çalıştığında API dokümantasyonuna şu adresten erişebilirsiniz:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📧 E-posta Yapılandırması

E-posta bildirimleri için SMTP ayarlarını `.env` dosyasında yapılandırın:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=sizin_email@gmail.com
SENDER_PASSWORD=uygulama_sifresi
```

**Not**: Gmail kullanıyorsanız, uygulama şifresi oluşturmanız gerekebilir.

## 🧪 Test Çalıştırma

```bash
cd backend
pytest tests/
```

## 🚀 Production Dağıtımı

### Backend
```bash
# Gunicorn ile production
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm run build
# dist/ klasörünü web sunucunuza yükleyin
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

docker ps
---

**Geliştirici**: Kaan
**Versiyon**: 1.0.0
**Son Güncelleme**: 2024
