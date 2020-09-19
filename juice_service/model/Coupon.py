from django.db import models
from django.core.validators import MinValueValidator



class Coupon(models.Model):
    code         =    models.CharField(max_length=15)
    amount     =    models.IntegerField(validators=[MinValueValidator(0)])
    valid_upto =    models.DateField()

    objects = models.Manager()

    def __str__(self):
        return self.code

    class Meta:
        db_table = "coupons"