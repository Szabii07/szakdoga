# Generated by Django 5.0.7 on 2024-09-08 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0027_post_dislikes_post_likes_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
    ]
