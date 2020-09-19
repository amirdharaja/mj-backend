from juice_service.models import User

from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

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


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'address_type',
            'home_number',
            'street',
            'area',
            'landmark',
            'city_id',
            'pincode_id',
        )

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class AvailableCitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name',)

class AvailablePincodeSerializer(ModelSerializer):
    class Meta:
        model = Pincode
        fields = ('id','pincode',)

class ContactRequestSerializer(ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ('name', 'email', 'phone', 'details')

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class ItemCommentSerializer(ModelSerializer):
    class Meta:
        model = ItemComment
        fields = '__all__'

class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('user', 'address', 'payment', 'total', 'status')

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'phone',
            'password',
            'first_name',
            'last_name',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class PhoneOTPSerializer(ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = '__all__'

class MainSlideImageSerializer(ModelSerializer):
    class Meta:
        model = MainSlideImage
        fields = '__all__'

class PageImageSerializer(ModelSerializer):
    class Meta:
        model = PageImage
        fields = ('image')