# Generated by Django 4.2.6 on 2023-11-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_product_featured_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='featured_image',
            field=models.ImageField(null=True, upload_to='featured_image'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='Image_url',
            field=models.ImageField(null=True, upload_to='products'),
        ),
    ]
