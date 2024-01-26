# Generated by Django 4.2.9 on 2024-01-14 15:40

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('firstname', models.CharField(max_length=250)),
                ('lastname', models.CharField(max_length=250)),
                ('username', models.CharField(default='user', max_length=250)),
                ('email', models.EmailField(db_column='email', max_length=250, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('postcode', models.IntegerField()),
                ('city', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('total_price', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(default='00:00')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.customer')),
                ('pizzas', models.ManyToManyField(to='backend.pizza')),
            ],
        ),
    ]