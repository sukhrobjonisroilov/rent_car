# Generated by Django 5.0.6 on 2024-06-02 08:58

import core.models.auth
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('fio', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=20)),
                ('seria_ps', models.CharField(max_length=10, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('g_year', models.DateField(blank=True, null=True, verbose_name='Guvohnoma Yili')),
                ('g_seria', models.CharField(blank=True, max_length=20, null=True, verbose_name='Guvohnoma Seriasi')),
                ('g_ctg', models.CharField(blank=True, max_length=3, null=True, verbose_name='Guvohnoma Toifasi')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user_type', models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', core.models.auth.UserMG()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('raqam', models.CharField(max_length=15, verbose_name='Davlat raqami')),
                ('xk', models.TextField(blank=True, null=True)),
                ('price', models.IntegerField(default=0, verbose_name='Kunlik ijara narxi')),
                ('status', models.BooleanField(default=True, verbose_name='Ijaraga mumkinmi?')),
                ('yili', models.IntegerField(default=2015, verbose_name='Ishlab chiqarilgan yil')),
                ('img', models.ImageField(upload_to='cars')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.brand')),
                ('ctg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='Arenda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(auto_now_add=True)),
                ('date_to', models.DateField(default='2024-06-03')),
                ('summa', models.BigIntegerField(default=0)),
                ('status', models.SmallIntegerField(choices=[(0, 'tasdiqlanmagan'), (1, 'tasdiqlangan'), (2, 'tugatilgan'), (3, 'Bekor qilingan')], default=0)),
                ('pay_type', models.CharField(choices=[('Naqt', 'Naqt'), ('Plastik', 'Plastik'), ("Bo'lib to'lash", "Bo'lib to'lash")], max_length=25)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.car')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Rent Card', max_length=128)),
                ('number', models.CharField(max_length=20)),
                ('mask', models.CharField(blank=True, max_length=20, null=True)),
                ('expire', models.CharField(max_length=5)),
                ('token', models.CharField(max_length=256, unique=True)),
                ('balance', models.BigIntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Monitoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tr_id', models.CharField(max_length=128, unique=True)),
                ('amount', models.IntegerField(default=0)),
                ('status', models.SmallIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to='core.card')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to='core.card')),
            ],
        ),
    ]
