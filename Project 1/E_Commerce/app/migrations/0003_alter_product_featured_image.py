# Generated by Django 4.2.6 on 2023-11-13 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_product_section_delete_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='featured_image',
            field=models.ImageField(null=True, upload_to='products'),
        ),
    ]