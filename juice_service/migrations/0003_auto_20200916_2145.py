# Generated by Django 2.2.14 on 2020-09-16 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juice_service', '0002_remove_cart_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='cart',
            name='start',
            field=models.DateField(null=True),
        ),
    ]
