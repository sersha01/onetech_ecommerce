# Generated by Django 4.0.1 on 2022-02-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0010_alter_order_payment_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.BooleanField(default=False, null=True),
        ),
    ]