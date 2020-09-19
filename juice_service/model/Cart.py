from django.db import models
from django.core.validators import MinValueValidator
from juice_service.models import User

from juice_service.model.Item import Item
from juice_service.model.Order import Order



class Cart(models.Model):

    user            =   models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    item             =   models.ForeignKey(Item, on_delete=models.CASCADE, unique=False)
    count           =   models.IntegerField(validators=[MinValueValidator(0)])
    weeks           =   models.IntegerField(validators=[MinValueValidator(0)])
    is_ordered     =   models.BooleanField(default=False)
    order             =   models.ForeignKey(Order, on_delete=models.CASCADE, unique=False, null=True)
    start              =   models.DateField(null=True)
    end              =   models.DateField(null=True)
    created_at   =   models.DateTimeField(auto_now_add=True, null=True)
    updated_at  =   models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return 'Cart for the User ID: {}'.format(self.user)

    class Meta:
        db_table = "carts"