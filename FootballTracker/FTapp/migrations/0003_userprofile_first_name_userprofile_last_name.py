# Generated by Django 5.0.7 on 2024-08-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0002_userprofile_looking_for_team_userprofile_position_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
