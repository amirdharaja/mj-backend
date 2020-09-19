from django.db import models



class Pincode(models.Model):

    pincode          =   models.CharField(null=False, blank=False, max_length=6)
    created_at      =   models.DateTimeField(auto_now_add=True, null=True)
    updated_at     =   models.DateTimeField(auto_now=True, null=True)
    

    objects = models.Manager()

    def __str__(self):
        return 'Pincode: {}'.format(self.pincode)

    class Meta:
        db_table = "available_pincodes"