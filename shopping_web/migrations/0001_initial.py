# Generated by Django 5.0 on 2023-12-31 03:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('discount', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.PositiveBigIntegerField()),
                ('address', models.TextField()),
                ('password', models.CharField(max_length=150)),
                ('image', models.ImageField(upload_to='profile_image/')),
                ('user_type', models.CharField(default='buyer', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('product_price', models.PositiveIntegerField()),
                ('product_category', models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('kids', 'kids')], max_length=100)),
                ('product_brand', models.CharField(choices=[('luvis', 'luvis'), ('Diesel', 'Diesel'), ('polo', 'polo')], max_length=100)),
                ('product_size', models.CharField(choices=[('s', 's'), ('l', 'l'), ('xl', 'xl'), ('xxl', 'xxl')], max_length=100)),
                ('product_desc', models.TextField()),
                ('product_fimage', models.ImageField(upload_to='product_image/')),
                ('product_bimage', models.ImageField(upload_to='product_image/')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_web.user')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('product_price', models.PositiveBigIntegerField()),
                ('product_qty', models.PositiveBigIntegerField(default=1)),
                ('total_price', models.PositiveBigIntegerField()),
                ('payment_status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_web.product')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_web.user')),
            ],
        ),
        migrations.CreateModel(
            name='Whishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_web.user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_web.product')),
            ],
        ),
    ]
