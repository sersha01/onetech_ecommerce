# Generated by Django 4.0.1 on 2022-02-16 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
