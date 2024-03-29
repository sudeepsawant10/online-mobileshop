# Generated by Django 3.2.9 on 2021-12-07 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1)),
                ('date', models.DateField()),
                ('total_amount', models.IntegerField()),
                ('status', models.CharField(choices=[('Ordered', 'Ordered'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='ordered', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=255)),
                ('short_description', models.CharField(max_length=255)),
                ('camera', models.CharField(max_length=32)),
                ('display', models.CharField(max_length=32)),
                ('memory', models.CharField(max_length=32)),
                ('processor', models.CharField(max_length=32)),
                ('os', models.CharField(max_length=32)),
                ('image', models.ImageField(upload_to='productimg')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('selling_price', models.IntegerField(blank=True, default=8000)),
                ('discount_price', models.IntegerField(default=8000)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('stars', models.IntegerField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.product')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_type', models.CharField(choices=[('COD', 'COD'), ('UPI', 'UPI'), ('Net Banking', 'Net Banking')], max_length=100)),
                ('card_number', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.IntegerField(default=5000)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.IntegerField(default=1)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('flat_no', models.CharField(blank=True, max_length=50, null=True)),
                ('building', models.CharField(blank=True, max_length=100, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('pin', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
