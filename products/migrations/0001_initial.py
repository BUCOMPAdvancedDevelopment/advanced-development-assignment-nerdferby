# Generated by Django 3.2.9 on 2021-12-20 23:54

import address.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0004_auto_20211215_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('desc', models.TextField(max_length=512)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('1', 'Order confirmed'), ('2', 'Awaiting dispatch'), ('3', 'Dispatched, awaiting courier'), ('4', 'With courier, awaiting delivery'), ('5', 'Out for delivery'), ('6', 'Order delivered and fulfilled')], default='1', max_length=1)),
                ('address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.address')),
            ],
        ),
    ]
