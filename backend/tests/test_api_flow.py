import pytest
import httpx
import uuid
import asyncio

# Sunucu Adresi
BASE_URL = "http://127.0.0.1:8000"

# Her testte farklı veri olsun diye rastgele string
RANDOM_STR = str(uuid.uuid4())[:8]
EMAIL = f"admin_{RANDOM_STR}@test.com"
PASSWORD = "testpassword123"

# Verileri testler arasında taşımak için sözlük
context = {}

@pytest.mark.asyncio
async def test_full_flow():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=20.0) as client:
        
        # ----------------------------------------------------------------
        # 1. KAYIT OL (Register)
        # ----------------------------------------------------------------
        print(f"\n[1] Kullanıcı Kaydı Yapılıyor: {EMAIL}")
        user_data = {
            "FullName": f"Test Admin {RANDOM_STR}",
            "Email": EMAIL,
            "Password": PASSWORD,
            "Role": "admin" # Ürün eklemek için admin olmalı
        }
        # Senin UserCreate şemana uygun aliaslar (FullName, Email vs.)
        resp = await client.post("/api/v1/users/", json=user_data)
        assert resp.status_code == 201, f"Kayıt Hatası: {resp.text}"
        context["user_id"] = resp.json()["UserID"]
        print("✅ Kayıt Başarılı.")

        # ----------------------------------------------------------------
        # 2. GİRİŞ YAP (Login)
        # ----------------------------------------------------------------
        print("\n[2] Giriş Yapılıyor...")
        login_data = {
            "username": EMAIL,
            "password": PASSWORD
        }
        resp = await client.post("/login", data=login_data)
        assert resp.status_code == 200, f"Login Hatası: {resp.text}"
        token_info = resp.json()
        context["token"] = token_info["access_token"]
        
        # Header'ı hazırla
        headers = {"Authorization": f"Bearer {context['token']}"}
        print("✅ Login Başarılı. Token alındı.")

        # ----------------------------------------------------------------
        # 3. MARKA EKLE (Brand)
        # ----------------------------------------------------------------
        print("\n[3] Marka Ekleniyor...")
        brand_data = {
            "BrandName": f"Rolex_{RANDOM_STR}",
            "Country": "Switzerland",
            "Description": "Luxury watches"
        }
        resp = await client.post("/api/v1/brands/", json=brand_data, headers=headers)
        assert resp.status_code == 201, f"Marka Ekleme Hatası: {resp.text}"
        context["brand_id"] = resp.json()["BrandID"]
        print(f"✅ Marka Eklendi. ID: {context['brand_id']}")

        # ----------------------------------------------------------------
        # 4. SAAT EKLE (Watch)
        # ----------------------------------------------------------------
        print("\n[4] Saat Ekleniyor...")
        watch_data = {
            "ModelName": f"Submariner {RANDOM_STR}",
            "Gender": "Male",
            "CaseMaterial": "Steel",
            "StrapMaterial": "Steel",
            "MovementType": "Automatic",
            "WaterResistance": "300m",
            "Price": 15000,
            "Stock": 5,
            "ImageUrl": "http://img.com/watch.jpg",
            "BrandID": context["brand_id"]
        }
        resp = await client.post("/api/v1/watches/", json=watch_data, headers=headers)
        assert resp.status_code == 201, f"Saat Ekleme Hatası: {resp.text}"
        context["watch_id"] = resp.json()["WatchID"]
        print(f"✅ Saat Eklendi. ID: {context['watch_id']}")

        # ----------------------------------------------------------------
        # 5. FAVORİYE EKLE (TESTİN ASIL AMACI)
        # ----------------------------------------------------------------
        print("\n[5] Favoriye Ekleniyor...")
        # Senin FavoriteCreate şemanda sadece "watch_id" var (küçük harf)
        fav_data = {
            "watch_id": context["watch_id"]
        }
        resp = await client.post("/api/v1/favorites/", json=fav_data, headers=headers)
        
        # Hata varsa detaylı görelim
        if resp.status_code != 201:
            print(f"❌ Favori Ekleme Hatası! Kod: {resp.status_code}")
            print(f"❌ Cevap: {resp.text}")
        
        assert resp.status_code == 201
        fav_resp = resp.json()
        # Modelde favoriteID küçük harfle başlıyor olabilir, response'a bakıyoruz
        context["fav_id"] = fav_resp.get("favoriteid") or fav_resp.get("favoriteID") or fav_resp.get("FavoriteID")
        print(f"✅ Favoriye Eklendi. Fav ID: {context['fav_id']}")

        # ----------------------------------------------------------------
        # 6. FAVORİLERİ LİSTELE VE KONTROL ET
        # ----------------------------------------------------------------
        print("\n[6] Favoriler Listeleniyor...")
        resp = await client.get("/api/v1/favorites/", headers=headers)
        assert resp.status_code == 200
        favorites = resp.json()
        
        # Eklediğimiz saat listede mi?
        found = False
        for item in favorites:
            # Response modelinde WatchID geliyor mu kontrol et
            if item.get("WatchID") == context["watch_id"]:
                found = True
                break
        
        if found:
            print("✅ BAŞARILI: Eklenen saat favoriler listesinde görüldü.")
        else:
            print("❌ HATA: Saat eklendi dendi ama listede yok!")
            print("Gelen Liste:", favorites)
            assert False, "Favori listede bulunamadı"

        # ----------------------------------------------------------------
        # 7. TEMİZLİK (Clean Up)
        # ----------------------------------------------------------------
        print("\n[7] Temizlik Yapılıyor...")
        # Favoriyi sil
        if context.get("fav_id"):
            await client.delete(f"/api/v1/favorites/{context['fav_id']}", headers=headers)
        
        # Saati sil
        await client.delete(f"/api/v1/watches/{context['watch_id']}", headers=headers)
        
        # Markayı sil
        await client.delete(f"/api/v1/brands/{context['brand_id']}", headers=headers)
        
        # Kullanıcıyı sil
        await client.delete(f"/api/v1/users/{context['user_id']}", headers=headers)
        
        print("\n🎉 TÜM TESTLER BAŞARIYLA TAMAMLANDI!")

if __name__ == "__main__":
    # Eğer direkt çalıştırılırsa (pytest olmadan)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_full_flow())