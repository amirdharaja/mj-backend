from django.db import models
from juice_service.models import User

from juice_service.model.Item import Item



class ItemComment(models.Model):

    user            =   models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    item             =   models.ForeignKey(Item, on_delete=models.CASCADE, unique=False)
    comment      =   models.CharField(max_length=512, blank=False)
    created_at    =   models.DateTimeField(auto_now_add=True, null=True)
    updated_at   =   models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return 'Comment by the User ID: {}'.format(self.user)

    class Meta:
        db_table = "item_comments"
