from fastapi import status
from .base import BaseAPIException

class WatchNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Saat bulunamadı."
        )
