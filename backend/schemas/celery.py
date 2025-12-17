from pydantic import BaseModel, Field
from typing import List

class CeleryProductDetail(BaseModel):
    # Bu adlar, CRUD fonksiyonunda products_list_for_email'e attığın adlarla eşleşmeli.
    name: str
    quantity: int
    price: float  # CRUD'da Decimal'den float'a çevirmiştik

# 2. Celery Görevine gönderilen ana sözlük yapısı
class CeleryOrderDetails(BaseModel):
    """Celery görevine gönderilen sipariş verilerini taşıyan model."""
    order_id: str = Field(..., description="Sipariş ID'si")
    customer_email: str = Field(..., description="Müşterinin e-posta adresi")
    total_price: float = Field(..., description="Siparişin toplam fiyatı (float)")
    products: List[CeleryProductDetail] = Field(..., description="Sipariş edilen ürün listesi")
