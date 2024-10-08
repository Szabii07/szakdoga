# Generated by Django 5.0.7 on 2024-09-08 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0032_remove_playerprofile_experience_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerprofile',
            name='experience_list',
        ),
        migrations.AddField(
            model_name='playerprofile',
            name='experience',
            field=models.TextField(blank=True, verbose_name='Tapasztalatok'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='description',
            field=models.TextField(verbose_name='Leírás'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='player_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to='FTapp.playerprofile'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Cím'),
        ),
        migrations.AlterField(
            model_name='playerprofile',
            name='user_profile',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='FTapp.userprofile'),
        ),
    ]
