# Generated by Django 5.0.7 on 2024-09-15 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0055_remove_coach_team_name_coach_team_alter_team_coach'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='team',
            new_name='team_name',
        ),
    ]
