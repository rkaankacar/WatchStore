from fastapi import status
from .base import BaseAPIException

class OrderNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Sipariş bulunamadı."
        )

class OrderAccessDenied(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Bu siparişe erişim yetkiniz yok."
        )

class OrderEmptyCart(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Sepetiniz boş, sipariş verilemez."
        )

class OrderInsufficientStock(BaseAPIException):
    def __init__(self, model_name: str, stock: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Stok yetersiz: {model_name} (Kalan: {stock})"
        )

class OrderCannotBeCancelled(BaseAPIException):
    def __init__(self, current_status: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Sipariş '{current_status}' durumunda olduğu için iptal edilemez."
        )

class OrderInvalidStatusUpdate(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Bu endpoint sadece 'İptal Edildi' durumu için kullanılabilir."
        )

class OrderSystemError(BaseAPIException):
    def __init__(self, detail: str = "Sipariş işlenirken sistemsel bir hata oluştu."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=detail
        )
