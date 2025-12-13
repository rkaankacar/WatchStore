import os

import json

import traceback

import iyzipay

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession



from backend.crud.crud_order import order

from backend.crud.crud_watch import watch

from backend.crud.crud_cart import cart_crud





IYZICO_API_URL = "sandbox-api.iyzipay.com"

IYZICO_API_KEY = os.getenv("IYZICO_API_KEY")

IYZICO_SECRET_KEY = os.getenv("IYZICO_SECRET_KEY")





class CRUDPayment:
    # -----------------------------

    # 1) ÖDEME FORMUNU OLUŞTURAN METOT

    # -----------------------------

    async def create_payment_form(self, db: AsyncSession, user_id: int):



        options = {

            "base_url": IYZICO_API_URL,

            "api_key": IYZICO_API_KEY,

            "secret_key": IYZICO_SECRET_KEY

        }

       

        cart_items = await cart_crud.get_multi_by_user(db, user_id=user_id)

        if not cart_items:

            raise HTTPException(status_code=400, detail="Sepet boş")



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

                "name": "Test",

                "surname": "User",

                "email": "test@example.com",

                "gsmNumber": "+905350000000",

                "identityNumber": "11111111111",

                "registrationAddress": "Test Adres",

                "ip": "85.34.78.112",

                "city": "İstanbul",

                "country": "Türkiye",

                "zipCode": "34000"

            },

            "shippingAddress": {

                "contactName": "Test User",

                "city": "İstanbul",

                "country": "Türkiye",

                "address": "Test Adres",

                "zipCode": "34000"

            },

            "billingAddress": {

                "contactName": "Test User",

                "city": "İstanbul",

                "country": "Türkiye",

                "address": "Test Adres",

                "zipCode": "34000"

            },

            "basketItems": basket_items

        }

       

        checkout_form_initialize = iyzipay.CheckoutFormInitialize()

        response = checkout_form_initialize.create(request, options)



        if response is None:

            raise HTTPException(status_code=500, detail="Iyzico'dan yanıt alınamadı")



        response_dict = json.loads(response.read().decode("utf-8"))



        if response_dict.get("status") == "failure":

            raise HTTPException(

                status_code=500,

                detail=f"Iyzico Hatası: {response_dict.get('errorMessage')} (Kod: {response_dict.get('errorCode')})"

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

                raise Exception("Iyzico API boş yanıt döndürdü.")



            response_dict = json.loads(response.read().decode("utf-8"))



        except Exception as e:

            traceback.print_exc()

            raise HTTPException(

                status_code=500,

                detail=f"Iyzico İletişim Hatası: {e.__class__.__name__} - {str(e)}"

            )



        print(f"--- [IYZICO RESPONSE] Status={response_dict.get('status')} Payment={response_dict.get('paymentStatus')}")



        # Ödeme başarılı mı?

        if response_dict.get("paymentStatus") != "SUCCESS":

            raise HTTPException(

                status_code=400,

                detail=f"Ödeme Başarısız: {response_dict.get('paymentStatus')}"

            )


        user_id_source = response_dict.get("conversationId")
        if not user_id_source:
            user_id_source = response_dict.get("basketId")
        # conversationId → user_id
        if user_id_source is None or user_id_source == '':
            raise HTTPException(
            status_code=400, 
            detail="Kullanıcı ID'si (conversationId veya basketId) Iyzico yanıtında eksik."
            )
        try:
            user_id = int(user_id_source)
        except (ValueError, TypeError): # Hatanın detaylı yakalanması
            raise HTTPException(status_code=400, detail="Conversation ID (Kullanıcı ID) formatı hatalı.")



        shipping_address = response_dict.get("shippingAddress", {}).get("address", "Adres Bilgisi Yok")



        print(f"--- [ORDER] Kullanıcı: {user_id}")



        # Siparişi oluştur

        try:

            new_order = await order.create_from_cart(

                db,

                user_id=user_id,

                shipping_address=shipping_address

            )



            print(f"--- [ORDER] Oluşturuldu: {new_order.OrderID}")



            return {

                "status": "success",

                "order_id": new_order.OrderID,

                "message": "Ödeme başarılı, sipariş oluşturuldu."

            }



        except HTTPException as e:

            raise e



        except Exception as e:

            traceback.print_exc()

            raise HTTPException(

                status_code=500,

                detail=f"Kritik Sipariş Hatası: {e.__class__.__name__} - {str(e)}"

            )





payment_crud = CRUDPayment()