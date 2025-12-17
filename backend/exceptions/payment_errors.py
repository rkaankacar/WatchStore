from fastapi import status
from .base import BaseAPIException

class PaymentCartEmpty(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Sepet boş"
        )

class PaymentIyzicoError(BaseAPIException):
    def __init__(self, message: str, code: str = None):
        detail = f"Iyzico Hatası: {message}"
        if code:
            detail += f" (Kod: {code})"
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=detail
        )

class PaymentIyzicoConnectionError(BaseAPIException):
    def __init__(self, error_detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Iyzico İletişim Hatası: {error_detail}"
        )

class PaymentFailed(BaseAPIException):
    def __init__(self, status_msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"Ödeme Başarısız: {status_msg}"
        )

class PaymentUserMissing(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Kullanıcı ID'si (conversationId veya basketId) Iyzico yanıtında eksik."
        )

class PaymentInvalidConversationId(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Conversation ID (Kullanıcı ID) formatı hatalı."
        )

class PaymentOrderError(BaseAPIException):
    def __init__(self, error_detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Kritik Sipariş Hatası: {error_detail}"
        )
