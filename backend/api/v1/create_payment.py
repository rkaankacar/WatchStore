from http.client import HTTPException
import traceback
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_async_db, get_current_user 
from backend.crud.crud_payment import payment_crud
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(tags=["Payment"])

@router.post("/create")
async def create_payment(
    db: AsyncSession = Depends(get_async_db), 
    current_user = Depends(get_current_user)
):
    """
    Kullanıcının sepetinden toplam fiyatı alır ve Iyzico test modunda checkoutFormContent döner.
    """
    checkout_content = await payment_crud.create_payment_form(db, user_id=current_user.UserID)
    # Burada direkt HTML içeriğini döndürüyoruz ki, frontend Iyzico'ya yönlendirmeyi yapsın.
    return {"checkoutFormContent": checkout_content}

     
@router.post("/callback") 
async def iyzico_callback(
    # Iyzico, token'ı POST body'de 'token' adıyla gönderir. FastAPI'de bunu Form ile yakalarız.
    token: str = Form(...), 
    db: AsyncSession = Depends(get_async_db)
):
    """
    Iyzico tarafından ödeme tamamlandıktan sonra çağrılan geri bildirim (callback) endpoint'i.
    Ödeme başarılıysa siparişi oluşturur ve müşteriyi Siparişlerim sayfasına yönlendirir.
    """
    
    # Başarılı ve başarısız yönlendirme adreslerinizi buraya tanımlayın
    SUCCESS_URL = "http://localhost:5173/profil" 
    FAILURE_URL = "http://localhost:5173/checkout"

    try:
        # LOG: İşlem başladı
        print("--- [ENDPOINT LOG] Callback endpoint'i çalışmaya başladı.")
        
        # 1. Ödeme ve Sipariş Oluşturma İşlemini Başlat
        # Bu işlem ödeme kontrolünü yapar, siparişi kaydeder, stoğu düşürür ve sepeti temizler.
        result = await payment_crud.handle_payment_callback(db, token=token)
        
        # LOG: İşlem başarılı
        print("--- [ENDPOINT LOG] handle_payment_callback başarıyla tamamlandı.")
        
        # 2. BAŞARILI DURUM: Müşteriyi doğrudan Siparişlerim sayfasına yönlendir.
        return RedirectResponse(
            url=f"{SUCCESS_URL}?order_id={result.get('order_id')}", 
            status_code=303 # HTTP 303 See Other, POST sonrası yönlendirme için en uygun koddur.
        )

    except HTTPException as e:
        # Ödeme BAŞARISIZ (Iyzico'dan gelen hata veya Stok Yetersizliği gibi CRUD hataları)
        print(f"--- [ENDPOINT HATA] HTTPException yakalandı. Detay: {e.detail}")
        error_detail = e.detail
        
        # Hata detayını QUERY parametresi ile hata sayfasına gönder.
        return RedirectResponse(
            url=f"{FAILURE_URL}?error={error_detail}", 
            status_code=303
        )
        
    except Exception as e:
        # KRİTİK HATA (Veritabanı bağlantısı koptu, kütüphane hatası, beklenmedik hata)
        
        # 1. Terminale Hata İzini Yazdır (Kesinlikle Görmeliyiz!)
        print("\n" + "="*50)
        print("!!! KRİTİK HATA YAKALANDI !!!")
        traceback.print_exc() 
        print(f"Hata Türü: {e.__class__.__name__}. Detay: {str(e)}")
        print("="*50 + "\n")
        
        # 2. Hata Detayını URL'ye Ekle
        error_detail = f"Kritik Hata: {e.__class__.__name__}. Detay: {str(e)}"
        
        # Kritik hatayı hata sayfasına yönlendir.
        return RedirectResponse(
            url=f"{FAILURE_URL}?error={error_detail}", 
            status_code=303
        )