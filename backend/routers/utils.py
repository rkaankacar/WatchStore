import shutil
import os
import uuid
from fastapi import File, UploadFile, APIRouter

router = APIRouter()
# Resim Yükleme Endpointi
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # 1. Dosya uzantısını al (jpg, png vs.)
    file_extension = file.filename.split(".")[-1]
    
    # 2. Benzersiz bir isim oluştur (Aynı isimli dosyalar çakışmasın diye)
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    # 3. Kaydedilecek yol
    file_location = f"backend/static/images/{unique_filename}"
    
    # 4. Dosyayı diske kaydet
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    # 5. Frontend'in erişebileceği URL'i döndür
    # Not: Port numaran farklıysa burayı güncelle (Genelde 8000)
    return {"url": f"http://127.0.0.1:8000/static/images/{unique_filename}"}