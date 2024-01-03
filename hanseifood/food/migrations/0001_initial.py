# Generated by Django 3.2.20 on 2024-01-03 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('kakao_id', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('kakao_name', models.TextField()),
                ('nickname', models.TextField()),
                ('is_admin', models.BooleanField(default=False)),
                ('role', models.CharField(max_length=1)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
            options={
                'db_table': 'day',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'db_table': 'meal',
            },
        ),
        migrations.CreateModel(
            name='PayInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.TextField()),
                ('order_id', models.TextField()),
                ('order_date', models.DateTimeField()),
                ('create_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'pay_info',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_info', models.TextField()),
                ('is_used', models.BooleanField()),
                ('used_at', models.DateTimeField()),
                ('create_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='UserTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.payinfo')),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.ticket')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_ticket',
            },
        ),
        migrations.CreateModel(
            name='DayMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_student', models.BooleanField()),
                ('is_additional', models.BooleanField(default=False)),
                ('day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.day')),
                ('meal_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.meal')),
            ],
            options={
                'db_table': 'day_meal',
            },
        ),
    ]
