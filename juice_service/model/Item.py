from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



class Item(models.Model):

    DISCOUNT_TYPE = [
        ('0', u'No discount'),
        ('%', u'%'),
        ('₹', u'₹'),
        ('w', u'w'),
    ]

    name = models.CharField(max_length=255, null=False, blank=False)
    weight = models.CharField(max_length=16, null=False, blank=False)
    slug = models.SlugField()
    image = models.FileField(upload_to='images/item_images', null=True, default='images/no_image.png',)
    is_available = models.BooleanField(default=True)
    count_per_week = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(21)])
    rate_per_bottle = models.FloatField(validators=[MinValueValidator(0.0)])
    rate_per_week = models.FloatField(validators=[MinValueValidator(0.0)])
    discount_type = models.CharField(choices=DISCOUNT_TYPE, max_length=1, default='0', null=True)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    description = models.TextField(null=True)
    total_sales_count = models.IntegerField(editable=False, default=0, validators=[MinValueValidator(0)])
    total_sales_amount = models.IntegerField(editable=False, default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "items"