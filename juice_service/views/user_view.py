from juice_service.models import User

from juice_service.model.Item import Item
from juice_service.model.Cart import Cart
from juice_service.model.Address import Address
from juice_service.model.AvailablePincode import Pincode
from juice_service.model.AvailableCity import City
from juice_service.model.Order import Order

from juice_service.helpers import get_cart_count, get_cart_total_amount
from datetime import datetime, timedelta, date
from pluck import pluck

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view, APIView
from rest_framework.status import (
    HTTP_200_OK as ok,
    HTTP_201_CREATED as created,
    HTTP_202_ACCEPTED as accepted,
    HTTP_304_NOT_MODIFIED as no_change,
    HTTP_400_BAD_REQUEST as bad_request,
    HTTP_401_UNAUTHORIZED as un_authorized,
    HTTP_403_FORBIDDEN as forbidden,
    HTTP_404_NOT_FOUND as not_found,
)
from juice_service.serializers import (
    AddressSerializer,
    AvailablePincodeSerializer,
    AvailableCitySerializer,
    UserSerializer,
    CartSerializer,
    OrderSerializer,
)


@permission_classes((IsAuthenticated,))
class UserAccount(APIView):

    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return Response({'status': False}, status=not_found)

        user = UserSerializer(user,  many=False)
        return Response({'status': True, 'data': user.data}, status=ok)

    def put(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return Response({'status': False}, status=not_found)

        user.first_name = request.data.get('first_name') if request.data.get(
            'first_name') else user.first_name
        user.last_name = request.data.get('last_name') if request.data.get(
            'last_name') else user.last_name
        user.email = request.data.get(
            'email') if request.data.get('email') else user.email

        user.save()
        return Response({'status': True}, status=ok)

    def delete(self, request, *args, **kwargs):
        User.objects.filter(id=request.user.id).delete()
        Token.objects.filter(user=request.user).delete()
        return Response({'status': True}, status=ok)


@permission_classes((IsAuthenticated,))
class CartFunction(APIView):

    def get(self, request, *args, **kwargs):
        all_carts = Cart.objects.filter(user=request.user, is_ordered=False)
        carts = []
        for d in all_carts:
            data = {
                'id': d.id,
                'name': d.item.name,
                'weight': d.item.weight,
                'count': d.count,
                'image': str(d.item.image),
                'weeks': d.weeks,
                'rate_per_bottle': d.item.rate_per_bottle,
                'rate_per_week': d.item.rate_per_week,
                'count_per_week': d.item.count_per_week,
                'discount':d.item.discount,
                'discount_type':d.item.discount_type,
            }
            carts.append(data)

        data = {
            'carts': carts,
            'cart_count': get_cart_count(request.user),
            'cart_total_amount': get_cart_total_amount(request.user),
        }
        return Response({'status': True, 'data': data}, status=ok)

    def post(self, request, *args, **kwargs):
        data = request.data['cart']
        is_exist = Cart.objects.filter(item=data['id'], weeks=data['weeks'], is_ordered=False).first()
        if is_exist:
            is_exist.count += 1
            is_exist.save()
            cart_count = get_cart_count(request.user)
            data = {'cart_count': cart_count, }
            return Response({'status': True, 'data': data, 'message': 'Success! Cart updated'}, status=ok)

        Cart(
            weeks=data['weeks'],
            count=1,
            item_id=data['id'],
            user_id=request.user.id,
        ).save()

        cart_count = get_cart_count(request.user)
        data = {'cart_count': cart_count, }
        return Response({'status': True, 'data': data, 'message': 'Success! Added into Cart'}, status=ok)

    def put(self, request, *args, **kwargs):
        data = request.data['cart']
        is_exist = Cart.objects.filter(id=data['id'], is_ordered=False).first()
        if is_exist and is_exist.count > 0:
            if data['add']:
                is_exist.count += 1
            else:
                is_exist.count -= 1

            if is_exist.count <= 0:
                is_exist.delete()
            else:
                is_exist.save()

            return Response({'status': True, 'message': 'Success! Cart updated'}, status=ok)

        return Response({'status': True, 'message': 'Cart item not found'}, status=not_found)

    def delete(self, request, cart_id, *args, **kwargs):
        Cart.objects.filter(id=cart_id, is_ordered=False).delete()
        return Response({'status': True}, status=ok)


@permission_classes((IsAuthenticated,))
class Checkout(APIView):

    def get(self, request, *args, **kwargs):
        all_carts = Cart.objects.filter(user=request.user, is_ordered=False)
        all_address = Address.objects.filter(user=request.user)
        all_city = City.objects.all()
        all_pincode = Pincode.objects.all()
        all_address = AddressSerializer(all_address, many=True)
        all_city = AvailableCitySerializer(all_city, many=True)
        all_pincode = AvailablePincodeSerializer(all_pincode, many=True)
        carts = []
        for d in all_carts:
            data = {
                'id': d.id,
                'name': d.item.name,
                'weight': d.item.weight,
                'count': d.count,
                'image': str(d.item.image),
                'weeks': d.weeks,
                'rate_per_bottle': d.item.rate_per_bottle,
                'rate_per_week': d.item.rate_per_week,
                'count_per_week': d.item.count_per_week,
                'discount':d.item.discount,
                'discount_type':d.item.discount_type,
            }
            carts.append(data)

        data = {
            'carts': carts,
            'address': all_address.data,
            'pincode': all_pincode.data,
            'city': all_city.data,
            'cart_count': get_cart_count(request.user),
            'cart_total_amount': get_cart_total_amount(request.user),
        }

        return Response({'status': True, 'data': data}, status=ok)

    def post(self, request):
        address_id = None
        new_order_id = None
        if 'existing_address_id' in request.data['data']:
            address_id = request.data['data']['existing_address_id']
        else:
            data = request.data['data']['address']
            new_address = Address(
                address_type=data['address_type'],
                home_number=data['home_number'],
                street=data['street'],
                area=data['area'],
                landmark=data['landmark'],
                city_id=data['city_id'],
                pincode_id=data['pincode_id'],
                user=request.user
            )
            new_address.save()
            address_id = new_address.id

        total_amount = get_cart_total_amount(request.user)

        next_date = datetime.today() + timedelta(days=1)
        if not address_id:
            return Response({'status': False, 'data': None, 'message': 'Address ID can not be Null'}, status=bad_request)

        new_order_data = {
            'user': request.user.id,
            'address': int(address_id),
            'payment': request.data['data']['payment_type'],
            'total': total_amount,
            'status': 'Confirmed' if request.data['data']['payment_type'] == 'COD' else 'Waiting'
        }
        serializer = OrderSerializer(data=new_order_data)

        if serializer.is_valid():
            new_order = serializer.save()
            new_order_id = new_order.id

        carts = Cart.objects.filter(user=request.user, is_ordered=False)
        item_ids = pluck(carts, 'item_id')
        items = Item.objects.filter(id__in=item_ids)

        if not new_order_id:
            return Response({'status': False, 'data': None, 'message': 'Order ID can not be Null'}, status=bad_request)

        for d in carts:
            end = next_date + timedelta(days=14)
            if d.weeks == 4:
                next_date + timedelta(days=28)
            elif d.weeks == 8:
                next_date + timedelta(days=56)

            d.is_ordered=True
            d.order_id=new_order_id
            d.start=next_date
            d.end=end
            d.save()
            for dd in items:
                if d.item_id == dd.id:
                    dd.total_sales_amount += d.weeks * d.count * dd.rate_per_week
                    dd.total_sales_count += d.weeks * d.count
                    dd.save()

        return Response({'status': True, 'data': None, 'message': 'Order placed successfully'}, status=ok)


@api_view(["get"])
@permission_classes((IsAuthenticated,))
def get_order(request, *args, **kwargs):
    orders = Order.objects.filter(user=request.user).order_by('-date', '-time')
    all_items = Cart.objects.filter(user=request.user, is_ordered=True)

    total, current, delivered = 0, 0, 0
    ordered_items = []
    for order in orders:
        total += 1
        if order.status == 'Delivered':
            delivered += 1
        else:
            current += 1
        items = []
        for item in all_items:
            if order.id == item.order_id:
                data = {
                    'id': item.id,
                    'name': item.item.name,
                    'order_id': item.order_id,
                    'weight': item.item.weight,
                    'count': item.count,
                    'weeks': item.weeks,
                    'rate': item.item.rate_per_week * item.weeks,
                    'start': item.start,
                    'end': item.end,
                    'status': 'Alive' if item.end > date.today() else 'Completed',
                }

                items.append(data)
        if not items:
            continue
        else:
            ordered_items.append(
                {
                    'order_id': order.id,
                    'payment': order.payment,
                    'status': order.status,
                    'total_cost': order.total,
                    'items': items,
                    'address':{
                        'address_type': order.address.address_type,
                        'home_number': order.address.home_number,
                        'street': order.address.street,
                        'area': order.address.area,
                        'landmark': order.address.landmark,
                        'city': order.address.city.name,
                        'pincode': order.address.pincode.pincode,
                    }
                }
            )

    orders_count = {
        'total': total,
        'current': current,
        'delivered': delivered,
    }
    data = {
        'cart_count': get_cart_count(request.user),
        'ordered_items': ordered_items,
        'orders_count': orders_count
    }
    return Response({'status': True, 'data': data}, status=ok)


@api_view(["post"])
@permission_classes((IsAuthenticated,))
def cart(request, *args, **kwargs):
    item = Item.objects.filter(id=request.data['id']).first()
    if item:
        if request.data['add']:
            Cart(
                weight=item.weight,
                count=1,
                rate=item.rate,
                item=item,
                user_id=request.user.id,
            ).save()
            return Response({'status': True,}, status=ok)
        else:
            Cart.objects.filter(item_id=request.data['id']).delete()
            return Response({'status': True,}, status=ok)
    else:
        return Response({'status': False,}, status=not_found)

