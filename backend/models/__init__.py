# backend/models/__init__.py

# 1. ÖNCE FAVORİLERİ YÜKLÜYORUZ (En kritik hamle bu!)
# Dosya adı: Favorite.py, Class adı: Favorites
from .favorites import favorites

# 2. Sonra bağımlı olmayan diğer parçalar
from .watches_images import watches_images
from .cart import cart
from .reviews import reviews
from .brands import brands
from .ordersdetails import ordersdetails

# 3. Sonra Saatler (Çünkü yukarıdakilerle ilişkisi var)
from .watches import watches

# 4. Sonra Siparişler
from .orders import orders
from .payments import payments

# 5. EN SON KULLANICI (Hepsini kapsıyor)

from .users import users