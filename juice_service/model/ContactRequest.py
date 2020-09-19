from django.db import models



class ContactRequest(models.Model):

    name        =   models.CharField(max_length=255, blank=True)
    email       =   models.CharField(max_length=100, blank=True)
    phone       =   models.CharField(max_length=13, blank=True)
    details     =   models.TextField(blank=True)
    created_at  =   models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return 'Contact Request By {}'.format(self.name)

    class Meta:
        db_table = "contact_requests"