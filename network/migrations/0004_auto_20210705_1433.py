# Generated by Django 3.2.5 on 2021-07-05 14:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='followed',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
    ]
