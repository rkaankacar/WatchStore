from fastapi import status
from .base import BaseAPIException

class CartItemNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Sepet öğesi bulunamadı."
        )

class CartAccessDenied(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Bu sepet öğesine erişim veya işlem yetkiniz yok."
        )
