# Generated by Django 2.2.4 on 2019-09-30 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190928_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='date',
        ),
        migrations.AddField(
            model_name='review',
            name='doneTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
