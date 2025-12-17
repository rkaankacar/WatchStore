/**
 * Hata mesajını ayrıştıran yardımcı fonksiyon.
 * Backend'den gelen farklı hata formatlarını (FastAPI detail, özel error.message vb.)
 * tek bir standart mesaj stringine çevirir.
 * 
 * @param {Object} error - Axios catch bloğundan gelen error objesi
 * @param {String} defaultMessage - Eğer hatadan hiçbir şey çıkarılamazsa dönecek varsayılan mesaj
 * @returns {String} Görüntülenecek hata mesajı
 */
export const getErrorMessage = (error, defaultMessage = "Bir hata oluştu.") => {
    if (!error.response) {
        return "Sunucuya ulaşılamıyor. Lütfen internet bağlantınızı kontrol edin.";
    }

    const { data, status } = error.response;

    // 1. ÖZEL BACKEND HATA FORMATI: { error: { message: "...", details: [...] } }
    if (data && data.error) {
        // Varsa validation detaylarını veya ana mesajı döndür
        if (data.error.details && Array.isArray(data.error.details) && data.error.details.length > 0) {
            return data.error.details[0]; // İlk detayı göster
        }
        if (data.error.message) {
            return data.error.message;
        }
    }

    // 2. STANDART FastAPI FORMATI: { detail: "..." veya [{msg: "..."}] }
    if (data && data.detail) {
        // Pydantic validation hatası array dönebilir
        if (Array.isArray(data.detail) && data.detail.length > 0) {
            return data.detail[0].msg || JSON.stringify(data.detail);
        }
        // String dönerse direkt döndür
        if (typeof data.detail === 'string') {
            return data.detail;
        }
    }

    // 3. HTTP KODLARINA GÖRE VARSAYILAN MESAJLAR
    switch (status) {
        case 400: return "İstek geçersiz. Lütfen bilgilerinizi kontrol edin.";
        case 401: return "Oturum süreniz dolmuş veya giriş yapmadınız.";
        case 403: return "Bu işlemi yapmaya yetkiniz yok.";
        case 404: return "İstenen veri veya sayfa bulunamadı.";
        case 422: return "Girdiğiniz veriler doğrulanamadı.";
        case 500: return "Sunucu taraflı bir hata oluştu. Lütfen daha sonra tekrar deneyin.";
        default: return defaultMessage;
    }
};
