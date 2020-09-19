from django.db import models



class PageImage(models.Model):

    image            =    models.FileField(upload_to='images/page_images', null=False)
    is_available    =    models.BooleanField(default=True)
    created_at      =    models.DateTimeField(auto_now_add=True, null=True)
    updated_at     =    models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "page_images"