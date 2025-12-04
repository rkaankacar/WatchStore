from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt # python-jose kütüphanesi
from backend.core.config import settings

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Kullanıcı ID'sini (subject) alır ve şifreli bir Token string'i üretir.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Varsayılan olarak 30 dakika geçerli olsun
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    # Token'ın içine koyacağımız veriler (Payload)
    # 'sub' (subject) standarttır, ID'yi buraya gömüyoruz.
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Şifreleme (İmzalama)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt