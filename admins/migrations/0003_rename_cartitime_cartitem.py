# Generated by Django 4.0.1 on 2022-02-14 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItime',
            new_name='CartItem',
        ),
    ]
