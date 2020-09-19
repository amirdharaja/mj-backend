from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import MinValueValidator
from juice_service.models import User



class PhoneOTP(models.Model):

    phone_regax = RegexValidator(regex=r'[3-9]\d{9}$', message='Enter valid phone number')
    phone = models.CharField(validators=[phone_regax], max_length=15, unique=True)
    otp = models.CharField(max_length=15, null=True, blank=True)
    count = models.IntegerField(default=1, help_text='Count, Number of OTP sent', validators=[MinValueValidator(0)])
    validated =    models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.phone) + str(self.otp)

    class Meta:
        db_table = "phone_otps"
