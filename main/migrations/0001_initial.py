# Generated by Django 2.2.4 on 2019-09-26 03:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('nickName', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('postNum', models.CharField(blank=True, max_length=100, null=True)),
                ('level', models.IntegerField(default=1)),
                ('exp', models.IntegerField(default=0)),
                ('longitude', models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('eventStartDate', models.CharField(blank=True, max_length=100, null=True)),
                ('eventEndDate', models.CharField(blank=True, max_length=100, null=True)),
                ('eventTime', models.TextField(blank=True, max_length=1000, null=True)),
                ('eventPlace', models.TextField(blank=True, max_length=1000, null=True)),
                ('discription', models.TextField(blank=True, max_length=1000, null=True)),
                ('mapx', models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True)),
                ('mapy', models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True)),
                ('tel', models.CharField(blank=True, max_length=255, null=True)),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
                ('grade', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityTemp',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('eventStartDate', models.CharField(blank=True, max_length=100, null=True)),
                ('eventEndDate', models.CharField(blank=True, max_length=100, null=True)),
                ('eventTime', models.TextField(blank=True, max_length=1000, null=True)),
                ('eventPlace', models.TextField(blank=True, max_length=1000, null=True)),
                ('discription', models.TextField(blank=True, max_length=1000, null=True)),
                ('mapx', models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True)),
                ('mapy', models.DecimalField(blank=True, decimal_places=12, max_digits=20, null=True)),
                ('tel', models.CharField(blank=True, max_length=255, null=True)),
                ('img', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('level', models.IntegerField(default=0)),
                ('img', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('text', models.CharField(blank=True, max_length=100, null=True)),
                ('img', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Title',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('title_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Title')),
                ('user_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_Preference',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('preference_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Preference')),
                ('user_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_Activity',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('questDone', models.BooleanField(default=False)),
                ('reviewDone', models.BooleanField(default=False)),
                ('doneTime', models.DateTimeField(blank=True, null=True)),
                ('activity_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Activity')),
                ('user_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('user_nickName', models.CharField(blank=True, max_length=100, null=True)),
                ('text', models.TextField(blank=True, max_length=1000, null=True)),
                ('grade', models.IntegerField(blank=True, default=0, null=True)),
                ('activity_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Activity')),
                ('user_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Activity_Preference',
            fields=[
                ('num', models.AutoField(primary_key=True, serialize=False)),
                ('activity_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Activity')),
                ('preference_num', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Preference')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='character_num',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Character'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='title_num',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Title'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
