from django.db import models
from juice_service.models import User

from juice_service.model.AvailableCity import City
from juice_service.model.AvailablePincode import Pincode



class Address(models.Model):

    ADDRESS_CHOICES = (
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Other', 'Other')
    )

    user                              =    models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    address_type                 =    models.CharField(max_length=8, choices=ADDRESS_CHOICES)
    home_number               =    models.CharField(max_length=16, null=False)
    street                            =    models.CharField(max_length=255, null=False)
    area                              =    models.CharField(max_length=255, null=False)
    city                               =    models.ForeignKey(City, on_delete=models.CASCADE, unique=False)
    landmark                       =    models.CharField(max_length=255, null=False)
    pincode                          =    models.ForeignKey(Pincode, on_delete=models.CASCADE, unique=False)

    objects = models.Manager()

    def __str__(self):
        return 'Address for User: {}'.format(self.user)

    class Meta:
        db_table = "address"
