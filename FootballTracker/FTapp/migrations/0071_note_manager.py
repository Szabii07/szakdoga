# Generated by Django 5.0.7 on 2024-09-22 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0070_remove_note_post_note_created_at_note_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='manager',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='FTapp.manager'),
        ),
    ]
