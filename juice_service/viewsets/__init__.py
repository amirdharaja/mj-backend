from juice_service.models import User

from rest_framework.viewsets import ModelViewSet

from juice_service.model.Address import Address
from juice_service.model.AvailableCity import City
from juice_service.model.AvailablePincode import Pincode
from juice_service.model.Cart import Cart
from juice_service.model.ContactRequest import ContactRequest
from juice_service.model.Coupon import Coupon
from juice_service.model.ItemComment import ItemComment
from juice_service.model.Item import Item
from juice_service.model.Order import Order
from juice_service.model.PhoneOTP import PhoneOTP
from juice_service.model.MainSlideImage import MainSlideImage
from juice_service.model.PageImage import PageImage
from juice_service.serializers import (
    AddressSerializer,
    AvailableCitySerializer,
    AvailablePincodeSerializer,
    CartSerializer,
    ContactRequestSerializer,
    CouponSerializer,
    ItemCommentSerializer,
    ItemSerializer,
    OrderSerializer,
    PhoneOTPSerializer,
    MainSlideImageSerializer,
    PageImageSerializer,
    UserSerializer,
)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AvailableCityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = AvailableCitySerializer

class AvailablePincodeViewSet(ModelViewSet):
    queryset = Pincode.objects.all()
    serializer_class = AvailablePincodeSerializer

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class ContactRequestViewSet(ModelViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer

class CouponViewSet(ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class ItemCommentViewSet(ModelViewSet):
    queryset = ItemComment.objects.all()
    serializer_class = ItemCommentSerializer

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PhoneOTPViewSet(ModelViewSet):
    queryset = PhoneOTP.objects.all()
    serializer_class = PhoneOTPSerializer

class MainSlideImageViewSet(ModelViewSet):
    queryset = MainSlideImage.objects.all()
    serializer_class = MainSlideImageSerializer

class PageImageViewSet(ModelViewSet):
    queryset = PageImage.objects.all()
    serializer_class = PageImageSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
