# Generated by Django 4.2.6 on 2024-03-02 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_address_user_address2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='villlage',
            field=models.CharField(choices=[('Kangazha', 'Kangazha'), ('Karukachal', 'Karukachal'), ('Kurichy', 'Kurichy'), ('Madappally', 'Madappally'), ('Nedumkunnam', 'Nedumkunnam'), ('Thottackad', 'Thottackad'), ('Vakathanam', 'Vakathanam'), ('Vazhappally Padinjaru', 'Vazhappally Padinjaru'), ('Vazhoor', 'Vazhoor'), ('Vellavoor', 'Vellavoor')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pincodee',
            field=models.CharField(max_length=10),
        ),
    ]
