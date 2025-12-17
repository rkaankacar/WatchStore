from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

# --- PAYMENT (ÖDEME KAYITLARI) ---
class PaymentBase(BaseModel):
    order_id: int = Field(..., alias="OrderID")
    user_id: int = Field(..., alias="UserID")
    
    amount: Decimal = Field(..., decimal_places=2, description="Tahsil edilen miktar")
    status: str = Field(..., description="Ödeme durumu (Pending, Successful, Failed, Refunded)")

    iyzico_ref_id: Optional[str] = Field(None, alias="IyzicoRefId", max_length=100)
    conversation_id: str = Field(..., alias="ConversationID", max_length=100)
    auth_code: Optional[str] = Field(None, alias="AuthCode", max_length=50)

    raw_response: Optional[dict] = Field(None, description="Iyzico'dan dönen JSON cevabının tamamı")


class PaymentResponse(PaymentBase):
    id: int = Field(..., alias="PaymentID")
    payment_date: datetime = Field(..., alias="PaymentDate")
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# --- IYZICO ENTEGRASYON SCHEMALARI ---

# --- 5.1 Adres Verisi (Iyzico'ya gönderilecek basit adres formatı) ---
class AddressDataSchema(BaseModel):
    """Sipariş/Fatura Adresi Verisi."""
    full_name: str 
    address: str
    city: str
    zip: str
    
    model_config = ConfigDict(from_attributes=True)


# --- 5.2 Frontend'den gelen Iyzico Başlatma Verisi ---
class AddressAndUserInfoSchema(BaseModel):
    """
    Frontend'den gelen adres, GSM ve TC kimlik bilgisi (Iyzico için kritik).
    """
    # Adres bilgileri
    full_name: str = Field(..., description="Alıcının tam adı.")
    address: str = Field(..., description="Açık adres.")
    city: str = Field(..., description="Şehir.")
    zip: str = Field(..., description="Posta kodu.")
    
    # Iyzico için zorunlu kullanıcı bilgileri
    gsm_number: str = Field(..., description="GSM Numarası.")
    identity_number: str = Field(..., description="TC Kimlik Numarası (veya yurtdışı ID).")
    
    model_config = ConfigDict(from_attributes=True)
