# Generated by Django 4.0.1 on 2022-02-19 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_address_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='male-avatar.jpg', upload_to='profile_pic'),
        ),
    ]