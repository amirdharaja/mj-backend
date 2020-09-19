from django.db import models



class City(models.Model):

    name             =   models.CharField(max_length=255, null=False, blank=False)
    created_at      =   models.DateTimeField(auto_now_add=True, null=True)
    updated_at     =   models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return 'City: {}'.format(self.name)

    class Meta:
        db_table = "available_cities"