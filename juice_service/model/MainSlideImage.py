from django.db import models



class MainSlideImage(models.Model):

    image            =    models.FileField(upload_to='images/main_slide_images', null=False)
    is_available    =    models.BooleanField(default=True)
    created_at      =    models.DateTimeField(auto_now_add=True, null=True)
    updated_at     =    models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = "main_slide_images"