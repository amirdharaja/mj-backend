from django.db import models
from django.core.validators import MinValueValidator
from juice_service.models import User

from juice_service.model.Item import Item
from juice_service.model.Address import Address



class Order(models.Model):

    STATUS = [
	    ('', u'-------'),
        ('Pending', u'Pending'),
   	    ('Confirmed', u'Confirmed'),
        ('Out for Delivery', u'Out for Delivery'),
   	    ('Delivered', u'Delivered'),
   	    ('Canceled', u'Canceled'),
	]
    PAYMENT_CHOICES = (
        ('COD', 'Cash On Delivery'),
        ('UPI', 'UPI'),
        ('Card', 'Card')
    )


    user             =   models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    address        =   models.ForeignKey(Address, on_delete=models.CASCADE, unique=False)
    payment       =   models.CharField(choices=PAYMENT_CHOICES, max_length=32, null=False, default='COD')
    status           =   models.CharField(choices=STATUS, max_length=16, null=False, default='Pending')
    total             =   models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    date              =   models.DateField(null=True, auto_now_add=True)
    time              =   models.TimeField(null=True, auto_now_add=True)
    created_at     =   models.DateTimeField(auto_now_add=True, null=True)
    updated_at    =   models.DateTimeField(auto_now=True, null=True)


    objects = models.Manager()

    def __str__(self):
        return 'Order by the User ID: {}'.format(self.user)

    class Meta:
        db_table = "orders"