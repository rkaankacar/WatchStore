from fastapi import status
from .base import BaseAPIException

class UserNotFound(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Kullanıcı bulunamadı."
        )

class UserAlreadyExists(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Bu email adresi zaten kullanılıyor."
        )

class PasswordIncorrect(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Mevcut şifre yanlış!"
        )

class PasswordMismatch(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Yeni şifreler aynı değil!"
        )

class PasswordSame(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Yeni şifre mevcut şifre ile aynı olamaz!"
        )
