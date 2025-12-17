from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str       # Frontend yönlendirmesi için
    user_id: int  
    name: str# State yönetimi için
