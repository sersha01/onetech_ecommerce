# Generated by Django 4.0.1 on 2022-03-09 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0025_order_coupen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupen',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
