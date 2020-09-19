from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from juice_service.viewsets import (
    AddressViewSet,
    AvailableCityViewSet,
    AvailablePincodeViewSet,
    ContactRequestViewSet,
    CartViewSet,
    CouponViewSet,
    ItemCommentViewSet,
    ItemViewSet,
    OrderViewSet,
    PhoneOTPViewSet,
    MainSlideImageViewSet,
    PageImageViewSet,
    UserViewSet,
)

router = DefaultRouter()

router.register('all/address/', AddressViewSet)
router.register('all/city/', AvailableCityViewSet)
router.register('all/pincode/', AvailablePincodeViewSet)
router.register('all/contact-requests/', ContactRequestViewSet)
router.register('all/cart/', CartViewSet)
router.register('all/coupon/', CouponViewSet)
router.register('all/commet/', ItemCommentViewSet)
router.register('all/item/', ItemViewSet)
router.register('all/orders/', OrderViewSet)
router.register('all/otp/', PhoneOTPViewSet)
router.register('all/main-slide-image/', MainSlideImageViewSet)
router.register('all/page-image/', PageImageViewSet)
router.register('all/users/', UserViewSet)


app_name = 'juice_service'

from juice_service.views.auth_view import (
    ValidatePhoneSendOTP,
    ValidateOTP,
    Register,
    login,
    ResendOTP,
)
from juice_service.views.common_view import (
    Home,
    products,
    get_item,
    send_contact_request,
    get_best_selling_products,
    get_page_images,
)
from juice_service.views.user_view import (
    CartFunction,
    Checkout,
    UserAccount,
    get_order,
    cart
)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', login, name='login'),
    path('resend/otp/', ResendOTP.as_view(), name='resend_otp'),
    re_path(r'validate/phone/', ValidatePhoneSendOTP.as_view()),
    re_path(r'validate/otp/', ValidateOTP.as_view()),
    re_path(r'register/', Register.as_view()),
    path(r'home/', Home.as_view()),

    path('my/account/', UserAccount.as_view(), name='my_account'),

    path('products/', products, name='products'),
    # path('category/<str:category_name>/<int:category_id>/all-items/<int:sub_category_id>/<int:item_id>/', get_item, name='get_item'),
    # path('category/<str:category_name>/<int:category_id>/all-items/<int:sub_category_id>/', products, name='get_sub_items'),

    path('cart/', CartFunction.as_view(), name='get_cart'),
    path('add/cart/', CartFunction.as_view(), name='add_cart'),
    path('update/cart/', CartFunction.as_view(), name='update_cart'),
    path('remove/cart/<int:cart_id>/', CartFunction.as_view(), name='delete_cart'),

    path('checkout/', Checkout.as_view(), name='checkout'),
    path('order/checkout/', Checkout.as_view(), name='order-checkout'),
    path('orders/', get_order, name='get_order'),

    path('contact/', send_contact_request, name='send_contact_request'),
    path('best-selling-products/', get_best_selling_products, name='get_best_selling_products'),

    path('<int:sub_category_id>/<str:item_slug>/<int:item_id>/', get_item, name='get_item'),
    path('handle/cart/', cart, name='cart'),
    path('page/images/', get_page_images, name='get_page_images'),



]