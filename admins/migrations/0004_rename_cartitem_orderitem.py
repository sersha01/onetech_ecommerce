# Generated by Django 4.0.1 on 2022-02-14 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0003_rename_cartitime_cartitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CartItem',
            new_name='OrderItem',
        ),
    ]
