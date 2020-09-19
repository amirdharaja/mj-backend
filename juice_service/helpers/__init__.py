from juice_service.models import User
from juice_service.model.Cart import Cart

from rest_framework.authtoken.models import Token

from datetime import timedelta
from django.utils import timezone
from django.conf import settings

import random
import requests

def get_cart_count(user):
    qs = Cart.objects.filter(user=user, is_ordered=False)
    cart_count = 0
    if qs.exists():
        for d in qs:
            cart_count += d.count
    return cart_count

def get_cart_total_amount(user):
    qs = Cart.objects.filter(user=user, is_ordered=False)
    total = 0
    if qs.exists():
        for d in qs:
            total += d.count * d.item.rate_per_week * d.weeks
    return total

def sent_otp(phone):
    if phone:
        phone = '+91' + phone
        key = random.randint(100000, 999999)
        OTP_LINK = 'http://sms.maximaa.biz/api/sendhttp.php?authkey=16921AzzqY6rJ5f3a78ffP15&mobiles={}&message=OTP:{}&sender=MOTHER&route=4'.format(phone, key)
        requests.get(OTP_LINK)
        return key
    else:
        return False

def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

def verify_token(token):
    is_expired = is_token_expired(token)
    print(token.user,'******', token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token