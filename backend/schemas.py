from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# =============================================================================
# 1. BASE & SIMPLE RESPONSE MODELLERİ (DÖNGÜ KIRICILAR)
# =============================================================================

# --- BRAND BASE ---
class BrandBase(BaseModel):
    name: str = Field(..., alias="BrandName")
    country: str = Field(..., alias="Country")
    description: str = Field(..., alias="Description")

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    name: Optional[str] = Field(None, alias="BrandName")
    country: Optional[str] = Field(None, alias="Country")
    description: Optional[str] = Field(None, alias="Description")

class BrandSimpleResponse(BrandBase):
    id: int = Field(..., alias="BrandID")
    created_at: datetime = Field(..., alias="CreatedAt")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- WATCH IMAGE BASE ---
class WatchImageBase(BaseModel):
    image_url: str = Field(..., alias="ImageUrl")

class WatchImageCreate(WatchImageBase):
    watch_id: int = Field(..., alias="WatchID")

class WatchImageUpdate(BaseModel):
    image_url: Optional[str] = Field(None, alias="ImageUrl")

class WatchImageSimpleResponse(WatchImageBase):
    id: int = Field(..., alias="ImageID")
    watch_id: int = Field(..., alias="WatchID")
    created_at: datetime = Field(..., alias="CreatedAt")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- USER BASE & SIMPLE ---
class UserBase(BaseModel):
    full_name: str = Field(..., alias="FullName")
    email: EmailStr = Field(..., alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")
    role: str = Field(default="user", alias="Role")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, alias="Password")

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, alias="FullName")
    email: Optional[EmailStr] = Field(None, alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")

class UserSimpleResponse(BaseModel):
    id: int = Field(..., alias="UserID")
    full_name: str = Field(..., alias="FullName")
    email: EmailStr = Field(..., alias="Email")
    phone: Optional[str] = Field(None, alias="Phone")
    address: Optional[str] = Field(None, alias="Address")
    city: Optional[str] = Field(None, alias="City")
    country: Optional[str] = Field(None, alias="Country")
    role: str = Field(..., alias="Role")
    created_at: datetime = Field(..., alias="CreatedAt")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="ignore",
        ignored_types=(list, dict)
    )



# --- WATCH BASE & SIMPLE ---
class WatchBase(BaseModel):
    model_name: str = Field(..., alias="ModelName")
    gender: str = Field(..., alias="Gender")
    case_material: str = Field(..., alias="CaseMaterial")
    strap_material: str = Field(..., alias="StrapMaterial")
    movement_type: str = Field(..., alias="MovementType")
    water_resistance: str = Field(..., alias="WaterResistance")
    description: Optional[str] = Field(None, alias="Description")
    price: Decimal = Field(..., alias="Price", gt=0)
    stock: int = Field(..., alias="Stock", ge=0)
    image_url: str = Field(..., alias="ImageUrl")

class WatchCreate(WatchBase):
    brand_id: int = Field(..., alias="BrandID")

class WatchUpdate(BaseModel):
    model_name: Optional[str] = Field(None, alias="ModelName")
    price: Optional[Decimal] = Field(None, alias="Price", gt=0)
    stock: Optional[int] = Field(None, alias="Stock", ge=0)
    brand_id: Optional[int] = Field(None, alias="BrandID")
    image_url: Optional[str] = Field(None, alias="ImageUrl")

class WatchSimpleResponse(WatchBase):
    id: int = Field(..., alias="WatchID")
    brand_id: int = Field(..., alias="BrandID")
    created_at: datetime = Field(..., alias="CreatedAt")
    
    brand: Optional[BrandSimpleResponse] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# =============================================================================
# 2. FULL RESPONSE MODELLERİ & TİCARİ MODELLER
# =============================================================================

# --- REVIEW (YORUMLAR) ---
class ReviewBase(BaseModel):
    rating: Decimal = Field(..., alias="Rating", ge=1, le=5)
    comment: Optional[str] = Field(None, alias="Comment")

class ReviewCreate(ReviewBase):
    watch_id: int = Field(..., alias="WatchID")

class ReviewUpdate(BaseModel):
    rating: Optional[Decimal] = Field(None, alias="Rating")
    comment: Optional[str] = Field(None, alias="Comment")

class ReviewResponse(ReviewBase):
    id: int = Field(..., alias="ReviewID")
    user_id: int = Field(..., alias="UserID")
    watch_id: int = Field(..., alias="WatchID")
    created_at: datetime = Field(..., alias="CreatedAt")
    
    user: Optional[UserSimpleResponse] = None 
    watch: Optional[WatchSimpleResponse] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- CART (SEPET) ---
class CartBase(BaseModel):
    quantity: int = Field(..., alias="Quantity", gt=0)

class CartCreate(CartBase):
    watch_id: int = Field(..., alias="WatchID")

class CartUpdate(BaseModel):
    quantity: int = Field(..., alias="Quantity", gt=0)

class CartResponse(CartBase):
    id: int = Field(..., alias="CartID")
    user_id: int = Field(..., alias="UserID")
    watch_id: int = Field(..., alias="WatchID")

    watch: Optional[WatchSimpleResponse] = None
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- ORDER DETAILS ---
class OrderDetailBase(BaseModel):
    quantity: int = Field(..., alias="Quantity", gt=0)
    unit_price: Decimal = Field(..., alias="UnitPrice", ge=0)

class OrderDetailCreate(OrderDetailBase):
    watch_id: int = Field(..., alias="WatchID")

class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = Field(None, alias="Quantity")

class OrderDetailResponse(OrderDetailBase):
    id: int = Field(..., alias="OrderDetailID")
    order_id: int = Field(..., alias="OrderID")
    watch_id: int = Field(..., alias="WatchID")

    watch: Optional[WatchSimpleResponse] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# --- ORDER (SİPARİŞ) ---
class OrderBase(BaseModel):
    total_amount: Decimal = Field(..., alias="TotalAmount") 
    status: str = Field(..., alias="Status")
    shipping_address: str = Field(..., alias="ShippingAddress")

class OrderCreate(OrderBase):
    user_id: int = Field(..., alias="UserID")

class OrderUpdate(BaseModel):
    Status: Optional[str]

class OrderResponse(OrderBase):
    id: int = Field(..., alias="OrderID")
    user_id: int = Field(..., alias="UserID")
    order_date: datetime = Field(..., alias="OrderDate")
    
    user: Optional[UserSimpleResponse] = None
    order_details: List[OrderDetailResponse] = []
    
    # Yeni: Payment ilişkisini ekleyelim (Order detayında Payment'ı görmek isteyebiliriz)
    # payments: List["PaymentResponse"] = [] # Forward reference gerekli olabilir

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


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
    
# Forward reference'ı düzeltmek için (Eğer OrderResponse'a PaymentResponse eklendiyse)
# OrderResponse.model_rebuild()


# =============================================================================
# 3. ANA MODELLERİN FULL VERSİYONLARI (MIRAS ALMA)
# =============================================================================

class BrandResponse(BrandSimpleResponse):
    watches: List[WatchSimpleResponse] = []

class WatchResponse(WatchSimpleResponse):
    images: List[WatchImageSimpleResponse] = []
    reviews: List[ReviewResponse] = []

class UserResponse(UserSimpleResponse):
    orders: List[OrderResponse] = []
    reviews: List[ReviewResponse] = []
    cart_items: List[CartResponse] = []
    

# =============================================================================
# 4. AUTH & FAVORITES SCHEMAS
# =============================================================================

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str       # Frontend yönlendirmesi için
    user_id: int  
    name: str# State yönetimi için
    
class FavoriteCreate(BaseModel):
    watch_id: int

class FavoriteResponse(BaseModel):
    FavoriteID: int = Field(..., alias="FavoriteID") 
    
    UserID: int
    WatchID: int
    
    user: Optional[UserSimpleResponse] = None 
    watch: Optional[WatchSimpleResponse] = None 
    
    model_config = ConfigDict(
        from_attributes=True, 
        populate_by_name=True
    )

# =============================================================================
# 5. IYZICO ENTEGRASYON SCHEMALARI (YENİ EKLEMELER) 🚀
# =============================================================================

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
    
class UserChangePassword(BaseModel):
    current_password: str 
    new_password: str 
    new_password_again: str 

    
