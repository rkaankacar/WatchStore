from fastapi import status
from .base import BaseAPIException

class FavoriteNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Favori öğesi bulunamadı."
        )

class FavoriteAccessDenied(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Bu favori öğesine erişim veya işlem yetkiniz yok."
        )
