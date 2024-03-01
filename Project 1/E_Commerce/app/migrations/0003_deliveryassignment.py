# Generated by Django 4.2.6 on 2024-02-27 09:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_date', models.DateField(auto_now_add=True)),
                ('delivery_man', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_deliveries', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_deliveries', to='app.product')),
            ],
        ),
    ]
