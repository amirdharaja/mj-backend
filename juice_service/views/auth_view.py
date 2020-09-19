from django.contrib.auth.models import auth

from juice_service.models import User
from juice_service.model.PhoneOTP import PhoneOTP

from juice_service.helpers import sent_otp, verify_token, expires_in, get_cart_count

from juice_service.serializers import (
    UserSerializer,
    PhoneOTPSerializer,
)

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import permission_classes, api_view, APIView
from rest_framework.status import (
    HTTP_200_OK as ok,
    HTTP_201_CREATED as created,
    HTTP_202_ACCEPTED as accepted,
    HTTP_400_BAD_REQUEST as bad_request,
    HTTP_401_UNAUTHORIZED as un_authorized,
    HTTP_403_FORBIDDEN as forbidden,
    HTTP_404_NOT_FOUND as not_found,
    HTTP_405_METHOD_NOT_ALLOWED as method_not_allowd,
    HTTP_429_TOO_MANY_REQUESTS as to_many_request,
    HTTP_502_BAD_GATEWAY as bad_gateway,
)

from datetime import datetime, timedelta


@permission_classes((AllowAny,))
class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        if phone:
            phone = str(phone)
            user = User.objects.filter(phone=phone).first()
            if user:
                return Response({'status': False, 'detail': 'Phone number already exist', }, status=bad_request)

            key = sent_otp(phone)
            if key:
                old = PhoneOTP.objects.filter(phone=phone).first()
                if old:
                    old.otp = key
                    old.count += 1
                    old.save()
                    if old.count > 10:
                        return Response({'status': False, 'detail': 'Sending OTP error. Please contact customer support', }, status=ok)

                    return Response({'status': True, 'detail': 'OTP sent successfully', }, status=ok)

                new = {
                    'phone': phone,
                    'otp': key
                }
                serializer = PhoneOTPSerializer(data=new)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'status': True, 'detail': 'OTP sent successfully', }, status=ok)
            return Response({'status': False, 'detail': 'Sending OTP error', }, status=bad_request)

        return Response({'status': False, 'detail': 'Phone number is required', }, status=bad_request)


@permission_classes((AllowAny,))
class ValidateOTP(APIView):

    def post(self, request, *args, **kwargs):
        otp_sent = request.data['otp']
        phone = request.data['phone']
        print(otp_sent, phone)
        user = User.objects.filter(phone=phone).first()
        if not user:
            user = User.objects.filter(email=phone).first()
            if not user:
                return Response({'status': False, 'detail': 'User not found', }, status=not_found)

        if otp_sent:
            old = PhoneOTP.objects.filter(phone=user.phone, otp=otp_sent).first()
            if old:
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({'status': True, 'detail': 'OTP matched. Please Continue', }, status=ok)
                return Response({'status': False, 'detail': 'OTP not matched. Retry', }, status=un_authorized)
            return Response({'status': False, 'detail': 'If you not recived OTP, Please retry', }, status=bad_request)
        return Response({'status': False, 'detail': 'Please give both phone and otp', }, status=bad_request)


@permission_classes((AllowAny,))
class ResendOTP(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        user = User.objects.filter(phone=username).first()
        if not user:
            user = User.objects.filter(email=username).first()
            if not user:
                return Response({'status': False, 'detail': 'User not found', }, status=not_found)

        key = sent_otp(user.phone)
        print(key)
        if key:
            PhoneOTP.objects.get_or_create(phone=user.phone)
            PhoneOTP.objects.update_or_create(phone=user.phone, defaults={"otp": key})
            return Response({'status': True, 'detail': 'OTP sent successfully', }, status=ok)

        return Response({'status': False, 'detail': 'Sending OTP error',}, status=bad_gateway)



@permission_classes((AllowAny,))
class Register(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data['data'])
        if serializer.is_valid():
            new_user = serializer.save()
            key = sent_otp(new_user.phone)
            if key:
                new = {
                    'phone': new_user.phone,
                    'otp': key
                }
                serializer = PhoneOTPSerializer(data=new)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                return Response({'status': True, 'detail': 'OTP sent successfully',}, status=ok)
            return Response({'status': False, 'detail': 'Sending OTP error',}, status=bad_gateway)
        return Response({'status': False, 'message':serializer.errors}, status=bad_request)

    @permission_classes((IsAuthenticated,))
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            return Response({'status': False, 'detail': 'User id not found', }, status=not_found)

        data = {
            'phone': user.phone,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'role': user.role,
        }
        data = {
            'user': data,
            'cart_count': get_cart_count(request.user.id),
        }
        return Response({'status': True, 'data': data, }, status=ok)

    def put(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({'status': False, 'detail': 'User "id" required', }, status=bad_request)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'status': False, 'detail': 'User id not found', }, status=not_found)

        user.phone = request.data.get(
            'phone') if request.data.get('phone') else user.phone
        user.first_name = request.data.get('first_name') if request.data.get(
            'first_name') else user.first_name
        user.last_name = request.data.get('last_name') if request.data.get(
            'last_name') else user.last_name
        user.email = request.data.get(
            'email') if request.data.get('email') else user.email
        user.active = False
        new = {'phone': request.data.get('phone')}
        serializer = PhoneOTPSerializer(data=new)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user.save()
        return Response({'status': True, 'detail': 'Successfully upudated, Please re login', }, status=ok)

    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({'status': False, 'detail': 'User "id" required', }, status=bad_request)

        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'status': False, 'detail': 'User id not found', }, status=not_found)

        user.delete()
        return Response({'status': True, 'detail': 'Successfully deleted', }, status=ok)


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both Phone number and password'}, status=bad_request)

    user = User.objects.filter(phone=username).first()
    if not user:
        user = User.objects.filter(email=username).first()
        if not user:
            return Response({'error': 'User not found. If you are a new user, Please register'}, status=not_found)

    validated = PhoneOTP.objects.filter(phone=user.phone).first()
    if not validated or not validated.validated:
        return Response({'error': 'Your Phone number is not verified'}, status=forbidden)

    user = auth.authenticate(phone=user.phone, password=password)
    if not user:
        return Response({'error': 'Invalid login Credentials'}, status=bad_request)

    token, _ = Token.objects.get_or_create(user=user)

    is_expired, token = verify_token(token)
    if is_expired:
        raise AuthenticationFailed("The Token is expired")

    data = {
        'id': user.id,
        'phone': user.phone,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

    return Response({
        'token': token.key,
        'data': data,
        'expires_in': expires_in(token),
        'status_code': ok
    },
        status=ok)
