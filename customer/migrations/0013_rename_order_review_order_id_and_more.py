# Generated by Django 4.0 on 2022-03-27 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_alter_review_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='order',
            new_name='order_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='product',
            new_name='product_id',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='user',
            new_name='user_id',
        ),
    ]
