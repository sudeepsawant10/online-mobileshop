# Generated by Django 4.0 on 2022-03-29 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0016_rename_user_address_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='address_id',
        ),
    ]
