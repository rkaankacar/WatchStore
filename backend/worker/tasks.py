# worker/tasks.py (SMTPLIB ile GÜNCELLENMİŞ VERSİYON)
import os
import smtplib # <-- Yeni kütüphane
import ssl     # <-- Yeni kütüphane
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import celery_app
from backend.schemas import CeleryOrderDetails 


# Ortam değişkenlerini al
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')


def create_invoice_html(details: CeleryOrderDetails) -> str: 
    """Sipariş detaylarını kullanarak HTML formatında bir fatura taslağı oluşturur."""
    
    product_rows = ""
    for product in details.products:
        product_rows += f"""
        <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">{product.name}</td>
            <td style="padding: 10px; border: 1px solid #ddd; text-align: center;">{product.quantity}</td>
            <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{product.price:.2f} TL</td>
            <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{(product.quantity * product.price):.2f} TL</td>
        </tr>
        """
        
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
            <h2 style="color: #007bff;">Siparişiniz Onaylandı!</h2>
            <p><strong>Değerli Müşterimiz,</strong></p>
            <p>Siparişiniz başarıyla alındı ve işleme konuldu. Sipariş No: {details.order_id}</p>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <thead>
                    <tr style="background-color: #007bff; color: white;">
                        <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Ürün Adı</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Adet</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Birim Fiyat</th>
                        <th style="padding: 10px; border: 1px solid #ddd;">Toplam</th>
                    </tr>
                </thead>
                <tbody>
                    {product_rows}
                    <tr style="font-weight: bold; background-color: #f0f0f0;">
                        <td colspan="3" style="padding: 10px; border: 1px solid #ddd; text-align: right;">Genel Toplam:</td>
                        <td style="padding: 10px; border: 1px solid #ddd; text-align: right;">{details.total_price:.2f} TL</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return html_content

@celery_app.task(name="send_order_email_task")
def send_order_email_task(order_details_dict: dict):
    
    details = CeleryOrderDetails(**order_details_dict)
    
    receiver_email = details.customer_email
    subject = f"Siparişiniz Onaylandı! (Sipariş No: {details.order_id})"
    html_body = create_invoice_html(details)
    
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    
    text = f"Siparişiniz onaylandı. Sipariş No: {details.order_id}. Toplam: {details.total_price:.2f} TL."
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html_body, "html")
    
    msg.attach(part1)
    msg.attach(part2)
    
    # KESİN ÇÖZÜM: SMTPLIB ile daha güvenilir gönderim ve hata yakalama
    context = ssl.create_default_context()
    
    try:
        # SMTP bağlantısı kuruluyor
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # TLS bağlantısını başlat
            server.starttls(context=context) 
            
            # Kimlik Doğrulama
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            # E-postayı Gönder
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
            
        print(f"✅ Celery Worker: E-posta {receiver_email} adresine başarıyla gönderildi (SMTPLIB)!")
        return True
    
    except smtplib.SMTPAuthenticationError:
        # Yanlış şifre/kullanıcı adı hatası buraya düşer
        print(f"❌ KESİN HATA: E-posta kimlik doğrulaması başarısız oldu. (Şifre/Kullanıcı adı yanlış!)")
        # Hata loglandıktan sonra görevi tekrar dene (Celery'nin varsayılan davranışı)
        raise
    except Exception as e:
        print(f"❌ Celery Worker: E-posta gönderilirken kritik hata oluştu: {e}")
        raise e