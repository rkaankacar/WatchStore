from fastapi import status
from .base import BaseAPIException

class ReviewNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Yorum bulunamadı."
        )

class ReviewAccessDenied(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Sadece kendi yorumunuzu silebilirsiniz."
        )
