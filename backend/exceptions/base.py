from typing import Any, Dict, Optional

class BaseAPIException(Exception):
    """
    Tüm özel API hataları için temel sınıf.
    HTTPException yerine bunu veya alt sınıflarını kullanacağız.
    """
    def __init__(
        self,
        status_code: int,
        message: str,
        payload: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.message = message
        self.payload = payload or {}
        super().__init__(message)
