# Generated by Django 5.0.1 on 2024-01-04 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_web', '0002_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
