# Generated by Django 4.0.1 on 2022-02-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0005_order_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='New', max_length=200, null=True),
        ),
    ]
