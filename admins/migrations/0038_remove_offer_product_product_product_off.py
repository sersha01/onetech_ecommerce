# Generated by Django 4.0.1 on 2022-03-30 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0037_remove_product_product_off_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='product_off',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='admins.offer'),
        ),
    ]