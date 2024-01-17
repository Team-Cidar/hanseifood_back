# Generated by Django 3.2.20 on 2024-01-17 18:54

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
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique_for_date=True)),
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
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('order_date', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
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
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='UserTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.payinfo', verbose_name='pay_id')),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.ticket', verbose_name='ticket_id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'user_ticket',
            },
        ),
        migrations.CreateModel(
            name='MenuLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_id', models.CharField(max_length=40)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'menu_like',
            },
        ),
        migrations.CreateModel(
            name='MenuComment',
            fields=[
                ('_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('menu_id', models.CharField(max_length=40)),
                ('comment', models.CharField(max_length=100)),
                ('commented_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'menu_comment',
            },
        ),
        migrations.CreateModel(
            name='DayMealDeleted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_type', models.CharField(default='N', max_length=1)),
                ('menu_id', models.CharField(max_length=40)),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
                ('day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.day', verbose_name='day_id')),
                ('meal_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.meal', verbose_name='meal_id')),
            ],
            options={
                'db_table': 'day_meal_deleted',
            },
        ),
        migrations.CreateModel(
            name='DayMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_type', models.CharField(default='N', max_length=1)),
                ('menu_id', models.CharField(max_length=40)),
                ('day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.day', verbose_name='day_id')),
                ('meal_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.meal', verbose_name='meal_id')),
            ],
            options={
                'db_table': 'day_meal',
            },
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_msg', models.CharField(max_length=30)),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food.menucomment', verbose_name='comment_id')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='reporter_id')),
            ],
            options={
                'db_table': 'comment_report',
            },
        ),
        migrations.CreateModel(
            name='CommentDeleted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_id', models.BigIntegerField(default=0, unique=True)),
                ('menu_id', models.CharField(max_length=40)),
                ('comment', models.CharField(max_length=100)),
                ('commented_at', models.DateTimeField()),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='user_id')),
            ],
            options={
                'db_table': 'comment_deleted',
            },
        ),
    ]
