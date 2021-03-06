# Generated by Django 4.0.1 on 2022-02-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0009_order_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='New', max_length=200, null=True),
        ),
    ]
