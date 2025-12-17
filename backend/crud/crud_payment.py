import os

import json

import traceback

import iyzipay
from datetime import datetime



from sqlalchemy.ext.asyncio import AsyncSession



from backend.crud.crud_order import order

from backend.crud.crud_watch import watch

from backend.crud.crud_cart import cart_crud
from backend.models.payments import payments # IMPORT EKLENDİ

from backend.exceptions import (
    PaymentCartEmpty,
    PaymentIyzicoError,
    PaymentIyzicoConnectionError,
    PaymentFailed,
    PaymentUserMissing,
    PaymentInvalidConversationId,
    PaymentOrderError
)



IYZICO_API_URL = "sandbox-api.iyzipay.com"

IYZICO_API_KEY = os.getenv("IYZICO_API_KEY")

IYZICO_SECRET_KEY = os.getenv("IYZICO_SECRET_KEY")





class CRUDPayment:
    # -----------------------------

    # 1) ÖDEME FORMUNU OLUŞTURAN METOT

    # -----------------------------

    async def create_payment_form(self, db: AsyncSession, user_id: int, address_data=None):



        options = {

            "base_url": IYZICO_API_URL,

            "api_key": IYZICO_API_KEY,

            "secret_key": IYZICO_SECRET_KEY

        }

       

        cart_items = await cart_crud.get_multi_by_user(db, user_id=user_id)

        if not cart_items:
            raise PaymentCartEmpty()



        total_price = 0.0

        basket_items = []



        for index, item in enumerate(cart_items):

            watch_obj = await watch.get(db, item.WatchID)

            price = float(getattr(watch_obj, "Price", 0.0))

            item_total = price * item.Quantity

            total_price += item_total



            basket_items.append({

                "id": str(item.CartID),

                "name": getattr(watch_obj, "Name", f"Ürün-{index}"),

                "category1": getattr(watch_obj.brand, "Name", "Genel Kategori") if watch_obj.brand else "Marka",

                "itemType": "PHYSICAL",

                "price": item_total

            })



        # Default/Test Değerler (Eğer frontend göndermezse)
        name = "Test"
        surname = "User"
        email = "test@example.com"
        gsm = "+905350000000"
        identity = "11111111111"
        address = "Test Adres"
        city = "İstanbul"
        country = "Türkiye"
        zip_code = "34000"
        
        if address_data:
            # AddressAndUserInfoSchema'dan gelen veriler
            # full_name'i name/surname olarak ayırmaya çalışalım (basitçe)
            full_name_parts = address_data.full_name.split(" ")
            if len(full_name_parts) > 1:
                name = " ".join(full_name_parts[:-1])
                surname = full_name_parts[-1]
            else:
                name = address_data.full_name
                surname = ""
                
            address = address_data.address
            city = address_data.city
            zip_code = address_data.zip
            
            # Zorunlu alanların override edilmesi
            if address_data.gsm_number: gsm = address_data.gsm_number
            if address_data.identity_number: identity = address_data.identity_number

        request = {
            "locale": "tr",
            "conversationId": str(user_id),
            "price": total_price,
            "paidPrice": total_price,
            "basketId": str(user_id),
            "paymentGroup": "PRODUCT",
            "callbackUrl": "https://esme-pseudoaffectionate-florine.ngrok-free.dev/api/v1/payment/callback",

            "buyer": {
                "id": str(user_id),
                "name": name,
                "surname": surname,
                "email": email,
                "gsmNumber": gsm,
                "identityNumber": identity,
                "registrationAddress": address,
                "ip": "85.34.78.112",
                "city": city,
                "country": country,
                "zipCode": zip_code
            },

            "shippingAddress": {
                "contactName": f"{name} {surname}",
                "city": city,
                "country": country,
                "address": address,
                "zipCode": zip_code
            },

            "billingAddress": {
                "contactName": f"{name} {surname}",
                "city": city,
                "country": country,
                "address": address,
                "zipCode": zip_code
            },

            "basketItems": basket_items
        }

       

        checkout_form_initialize = iyzipay.CheckoutFormInitialize()

        response = checkout_form_initialize.create(request, options)



        if response is None:
            raise PaymentIyzicoError("Iyzico'dan yanıt alınamadı")



        response_dict = json.loads(response.read().decode("utf-8"))



        if response_dict.get("status") == "failure":
            raise PaymentIyzicoError(
                message=response_dict.get('errorMessage'),
                code=response_dict.get('errorCode')
            )



        return response_dict.get("checkoutFormContent")



    # -----------------------------

    # 2) CALLBACK METODU (CLASS İÇİNE ALINDI)

    # -----------------------------

    async def handle_payment_callback(self, db: AsyncSession, token: str):



        print("--- [IYZICO CALLBACK] Başladı ---")



        options = {

            "base_url": IYZICO_API_URL,

            "api_key": IYZICO_API_KEY,

            "secret_key": IYZICO_SECRET_KEY

        }



        request = {

            "locale": "tr",

            "token": token

        }



        checkout_form = iyzipay.CheckoutForm()



        try:

            response = checkout_form.retrieve(request, options)



            if response is None:
                raise PaymentIyzicoError("Iyzico API boş yanıt döndürdü.")

            response_dict = json.loads(response.read().decode("utf-8"))

        except Exception as e:
            traceback.print_exc()
            if isinstance(e, PaymentIyzicoError):
                raise e
            raise PaymentIyzicoConnectionError(f"{e.__class__.__name__} - {str(e)}")



        print(f"--- [IYZICO RESPONSE] Status={response_dict.get('status')} Payment={response_dict.get('paymentStatus')}")



        # Ödeme başarılı mı?

        if response_dict.get("paymentStatus") != "SUCCESS":
            raise PaymentFailed(response_dict.get('paymentStatus'))


        user_id_source = response_dict.get("conversationId")
        if not user_id_source:
            user_id_source = response_dict.get("basketId")
        # conversationId → user_id
        if user_id_source is None or user_id_source == '':
            raise PaymentUserMissing()
            
        try:
            user_id = int(user_id_source)
        except (ValueError, TypeError): # Hatanın detaylı yakalanması
            raise PaymentInvalidConversationId()



        shipping_data = response_dict.get("shippingAddress", {})
        
        contact_name = shipping_data.get("contactName", "")
        addr_text = shipping_data.get("address", "")
        city = shipping_data.get("city", "")
        country = shipping_data.get("country", "")
        
        # Admin panelinde görünsün diye ismi de adrese ekliyoruz.
        shipping_parts = []
        if contact_name: shipping_parts.append(contact_name)
        if addr_text: shipping_parts.append(addr_text)
        if city: shipping_parts.append(city)
        if country: shipping_parts.append(country)
        
        shipping_address = " - ".join(shipping_parts).strip()

        if not shipping_address or shipping_address == "Adres Bilgisi Alınamadı":
             # FALLBACK: Iyzico bazen adresi boş dönebilir, bu durumda Kullanıcı profilindeki adresi alalım.
             try:
                 # Kullanıcıyı çek
                 from backend.crud.crud_user import user as user_crud
                 user_obj = await user_crud.get(db, id=user_id)
                 
                 if user_obj:
                     fallback_parts = []
                     if user_obj.Address: fallback_parts.append(user_obj.Address)
                     if user_obj.City: fallback_parts.append(user_obj.City)
                     if user_obj.Country: fallback_parts.append(user_obj.Country)
                     
                     if fallback_parts:
                         shipping_address = " - ".join(fallback_parts)
                         print(f"--- [ORDER] Iyzico adresi eksik, Kullanıcı profilden tamamlandı: {shipping_address}")
                     else:
                         shipping_address = "Adres Bilgisi Alınamadı (Profilde de yok)"
                 else:
                      shipping_address = "Adres Bilgisi Alınamadı"
                      
             except Exception as addr_ex:
                 print(f"--- [ORDER] Adres fallback hatası: {addr_ex}")
                 shipping_address = "Adres Bilgisi Alınamadı"



        print(f"--- [ORDER] Kullanıcı: {user_id}")



        # Siparişi oluştur

        try:

            new_order = await order.create_from_cart(

                db,

                user_id=user_id,

                shipping_address=shipping_address

            )



            # ID'yi erkenden sakla ki session rollback olsa bile elimizde olsun
            order_id_val = new_order.OrderID
            print(f"--- [ORDER] Oluşturuldu: {order_id_val}")

            # -----------------------------------------------------------
            # 3. ÖDEME KAYDINI OLUŞTUR (YENİ EKLENEN KISIM)
            # -----------------------------------------------------------
            try:
                # Iyzico response'dan gerekli alanları çekelim
                paid_price_str = response_dict.get("paidPrice", "0.0")
                if not paid_price_str: paid_price_str = "0.0"
                
                # ConversationID için Güçlü Fallback Mekanizması
                conv_id = response_dict.get("conversationId")
                if not conv_id:
                    conv_id = response_dict.get("basketId")
                if not conv_id:
                    conv_id = str(user_id)
                if not conv_id:
                    conv_id = "UNKNOWN"
                
                payment_rec = payments(
                    OrderID=order_id_val, # Sakladığımız ID'yi kullanıyoruz
                    UserID=user_id,
                    Amount=float(paid_price_str),
                    PaymentDate=datetime.now(),
                    Status="SUCCESS", # Zaten SUCCESS ise buradayız
                    IyzicoRefId=response_dict.get("paymentId"),
                    ConversationID=conv_id, # Asla null olmamasını garantiledik
                    AuthCode=response_dict.get("authCode"),
                    RawResponse=response_dict # Tüm JSON cevabını saklayalım (Opsiyonel ama faydalı)
                )
                db.add(payment_rec)
                await db.commit()
                # await db.refresh(payment_rec) # Gerekirse
                print(f"--- [PAYMENT] Kaydedildi: ID={payment_rec.PaymentID}")
                
            except Exception as pay_exc:
                # Ödeme kaydedilemese bile sipariş oluştu, müşteriye successful dönmeliyiz
                # Ancak hatayı loglayalım.
                print(f"!!! ÖDEME TABLOSUNA KAYIT HATASI: {pay_exc}")
                traceback.print_exc()
                # Hata olsa bile devam ediyoruz, çünkü sipariş başarılı.

            # -----------------------------------------------------------



            return {

                "status": "success",

                "order_id": order_id_val,  # Nesne üzerinden değil, değişkenden dönüyoruz

                "message": "Ödeme başarılı, sipariş oluşturuldu."

            }





        except Exception as e:
            # If it is one of our custom exceptions, re-raise it
            from backend.exceptions.base import BaseAPIException
            if isinstance(e, BaseAPIException):
                raise e
                
            traceback.print_exc()
            raise PaymentOrderError(f"{e.__class__.__name__} - {str(e)}")





payment_crud = CRUDPayment()