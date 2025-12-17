# Saat Satış E-Ticaret Platformu 🕐

Modern teknolojilerle geliştirilmiş, güvenli ve ölçeklenebilir bir online saat satış platformu. Backend tarafında FastAPI'nin asenkron gücünü, frontend tarafında ise React 19 ve Vite'ın hızını kullanır.

## 🌟 Özellikler

### 👤 Kullanıcı Deneyimi
- **Güvenli Kimlik Doğrulama**: JWT tabanlı kayıt ve giriş sistemi.
- **Profil Yönetimi**: Kullanıcı bilgileri, adres defteri ve şifre işlemleri.
- **Favoriler**: Beğenilen ürünleri kaydetme ve yönetme.
- **Değerlendirme Sistemi**: Ürünlere puan verme ve yorum yapma.
- **İade Süreci**: Kolay ve takip edilebilir ürün iade sistemi.

### 🛒 E-Ticaret Fonksiyonları
- **Gelişmiş Ürün Kataloğu**: Marka ve kategori bazlı filtreleme.
- **Akıllı Sepet**: Stok kontrollü sepet yönetimi.
- **Ödeme Entegrasyonu**: Iyzico ile güvenli kredi kartı ödemeleri.
- **Sipariş Takibi**: Sipariş durumu ve geçmiş sipariş detayları.

### 👨‍💻 Teknik Özellikler
- **Performans**: Asenkron veritabanı sorguları ve hızlı API yanıtları.
- **Arka Plan İşlemleri**: Celery ve Redis ile e-posta gönderimi gibi asenkron görevler.
- **Modern Frontend**: React 19, React Router v7 ve Bootstrap 5 ile responsive tasarım.

## 🛠️ Teknoloji Yığını

### Backend
- **Dil**: Python 3.8+
- **Framework**: FastAPI
- **Veritabanı**: PostgreSQL (AsyncPG sürücüsü ile)
- **ORM**: SQLAlchemy (Asenkron)
- **Şema Doğrulama**: Pydantic
- **Kuyruk Sistemi**: Redis & Celery
- **Ödeme**: Iyzipay (Iyzico)

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite
- **UI Kit**: Bootstrap 5
- **İkonlar**: Lucide React
- **HTTP İstemcisi**: Axios
- **Yönlendirme**: React Router DOM

## 📁 Proje Yapısı

```
saati-satis-yeni/
├── backend/
│   ├── api/v1/          # REST API endpointleri (auth, watches, cart, vb.)
│   ├── core/            # Config ve güvenlik ayarları
│   ├── crud/            # Veritabanı sorgu katmanı
│   ├── database/        # DB bağlantı oturumu
│   ├── models/          # SQLAlchemy veritabanı modelleri
│   ├── schemas/         # Pydantic veri şemaları
│   ├── static/          # Statik dosyalar
│   ├── worker/          # Celery worker yapılandırması
│   ├── main.py          # Uygulama giriş noktası
│   └── create_db_schema.py # Veritabanı kurulum scripti
├── frontend/
│   ├── src/             # React kaynak kodları
│   │   ├── components/  # Reusable bileşenler
│   │   ├── pages/       # Uygulama sayfaları
│   │   └── api.js       # API bağlantı noktası
│   ├── public/          # Statik assetler
│   └── vite.config.js   # Vite yapılandırması
├── requirements.txt     # Python bağımlılıkları
└── README.md
```

## 🚀 Kurulum ve Çalıştırma

### Ön Hazırlıklar
Aşağıdaki servislerin sisteminizde kurulu olduğundan emin olun:
- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis (Arka plan görevleri için)

### 1. Backend Kurulumu

Proje kök dizininde bir terminal açın:

```bash
# Sanal ortam oluşturma
python -m venv venv

# Sanal ortamı aktif etme
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükleme
pip install -r requirements.txt
```

**.env Dosyası Oluşturma**
`backend/.env` (veya kök dizinde, yapılandırmanıza göre) aşağıdaki içeriğe sahip bir dosya oluşturun:

```env
# Veritabanı
ASYNC_DATABASE_URL=postgresql+asyncpg://kullanici:sifre@localhost:5432/veritabani_adi
SCHEMA_NAME=saat_satis

# Güvenlik
SECRET_KEY=guclu_ve_gizli_bir_anahtar_olusturun
ALGORITHM=HS256

# Redis (Opsiyonel - Celery için)
REDIS_URL=redis://localhost:6379/0

# E-posta (Opsiyonel - Bildirimler için)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=sizin_email@gmail.com
SENDER_PASSWORD=uygulama_sifresi
```

**Veritabanını Hazırlama**

```bash
python backend/create_db_schema.py
```

**Uygulamayı Başlatma**

```bash
uvicorn backend.main:app --reload
```
API artık `http://localhost:8000` adresinde çalışmaktadır.
Swagger Dokümantasyonu: `http://localhost:8000/docs`

### 2. Frontend Kurulumu

Yeni bir terminal açın ve `frontend` klasörüne gidin:

```bash
cd frontend

# Paketleri yükleme
npm install

# Geliştirme sunucusunu başlatma
npm run dev
```
Uygulama `http://localhost:5173` adresinde yayına başlayacaktır.

## 🤝 Katkıda Bulunma

1. Bu depoyu fork edin.
2. Yeni bir feature branch oluşturun (`git checkout -b feature/YeniOzellik`).
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`).
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`).
5. Bir Pull Request oluşturun.

## 📝 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
