# Generated by Django 5.0.7 on 2024-09-11 09:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0033_remove_playerprofile_experience_list_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FTapp.userprofile'),
        ),
        migrations.AddField(
            model_name='post',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FTapp.userprofile'),
        ),
    ]
