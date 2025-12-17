from .brand import BrandBase, BrandCreate, BrandUpdate, BrandSimpleResponse, BrandResponse
from .watch import WatchImageBase, WatchImageCreate, WatchImageUpdate, WatchImageSimpleResponse, WatchBase, WatchCreate, WatchUpdate, WatchSimpleResponse, WatchResponse
from .user import UserBase, UserCreate, UserUpdate, UserChangePassword, UserSimpleResponse, UserResponse
from .review import ReviewBase, ReviewCreate, ReviewUpdate, ReviewResponse
from .cart import CartBase, CartCreate, CartUpdate, CartResponse
from .order import OrderDetailBase, OrderDetailCreate, OrderDetailUpdate, OrderDetailResponse, OrderBase, OrderCreate, OrderUpdate, OrderResponse
from .payment import PaymentBase, PaymentResponse, AddressDataSchema, AddressAndUserInfoSchema
from .returns import ReturnBase, ReturnCreate, ReturnUpdate, ReturnResponse
from .auth import Token
from .favorite import FavoriteCreate, FavoriteResponse
from .celery import CeleryProductDetail, CeleryOrderDetails

# Forward referansları çözmek için modelleri güncelle
# Forward referansları çözmek için modelleri güncelle
UserResponse.model_rebuild(
    _types_namespace={
        "OrderResponse": OrderResponse,
        "ReviewResponse": ReviewResponse,
        "CartResponse": CartResponse,
    }
)

WatchResponse.model_rebuild(
    _types_namespace={
        "ReviewResponse": ReviewResponse,
    }
)

BrandResponse.model_rebuild(
    _types_namespace={
        "WatchSimpleResponse": WatchSimpleResponse
    }
)
