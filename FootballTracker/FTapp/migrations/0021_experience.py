# Generated by Django 5.0.7 on 2024-09-08 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0020_alter_playerprofile_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Csapat   ')),
                ('description', models.TextField(verbose_name='Elért eredmény')),
                ('player_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='FTapp.playerprofile')),
            ],
        ),
    ]
