# Generated by Django 3.2.5 on 2021-07-09 07:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210707_0449'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-time']},
        ),
        migrations.AddField(
            model_name='profile',
            name='joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
