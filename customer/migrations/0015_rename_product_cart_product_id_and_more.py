# Generated by Django 4.0 on 2022-03-29 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_remove_cart_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='user',
            new_name='user_id',
        ),
    ]
