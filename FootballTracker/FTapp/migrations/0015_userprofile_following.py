# Generated by Django 5.0.7 on 2024-09-05 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0014_remove_playerprofile_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='FTapp.userprofile'),
        ),
    ]
