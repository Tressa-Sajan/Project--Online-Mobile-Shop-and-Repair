# Generated by Django 4.2.6 on 2024-03-04 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_village_deliveryman'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeliveryMan',
        ),
        migrations.DeleteModel(
            name='Village',
        ),
    ]