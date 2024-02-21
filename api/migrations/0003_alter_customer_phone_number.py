# Generated by Django 5.0.1 on 2024-02-20 12:41

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_order_amount_alter_order_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True, validators=[api.models.validate_phone_number]),
        ),
    ]