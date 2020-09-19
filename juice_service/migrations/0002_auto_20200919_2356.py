# Generated by Django 2.2.14 on 2020-09-19 18:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juice_service', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='rate_per_week',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]