from fastapi import status
from .base import BaseAPIException

class BrandNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Marka bulunamadı."
        )

class BrandAlreadyExists(BaseAPIException):
    def __init__(self, brand_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"'{brand_name}' isimli marka zaten mevcut."
        )
