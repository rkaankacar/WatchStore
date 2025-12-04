# core/errors.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

def register_exception_handlers(app: FastAPI):
    
    # 1. Bizim fırlattığımız HTTP Hataları (404, 400, 401 vb.)
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail, # Bizim yazdığımız "Kullanıcı bulunamadı" mesajı
                    "path": request.url.path
                }
            },
        )

    # 2. Pydantic Validasyon Hataları (422 - Eksik veri, yanlış tip vb.)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Pydantic'in karmaşık hatasını basitleştiriyoruz
        errors = []
        for error in exc.errors():
            field = error.get("loc")[-1] # Hatanın olduğu alan (örn: email)
            msg = error.get("msg")       # Hata mesajı (örn: field required)
            errors.append(f"{field}: {msg}")
            
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": 422,
                    "message": "Veri doğrulama hatası",
                    "details": errors,
                    "path": request.url.path
                }
            },
        )

    # 3. Beklenmeyen Sunucu Hataları (500 - Kod patlarsa)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Burada hatayı loglayabilirsin (print(exc) veya logger.error(exc))
        print(f"❌ SUNUCU HATASI: {exc}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": 500,
                    "message": "Sunucu taraflı bir hata oluştu. Lütfen daha sonra tekrar deneyin.",
                    "path": request.url.path
                }
            },
        )