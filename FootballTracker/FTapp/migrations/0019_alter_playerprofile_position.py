# Generated by Django 5.0.7 on 2024-09-08 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FTapp', '0018_rename_sent_at_message_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerprofile',
            name='position',
            field=models.CharField(choices=[('GK', 'Kapus'), ('RB', 'Jobbhátvéd'), ('CB', 'Középhátvéd'), ('LB', 'Balahátvéd'), ('CDM', 'Védekező középpályás'), ('CM', 'Középpályás'), ('CAM', 'Támadó középpályás'), ('RW', 'Jobbszélső'), ('LW', 'Balszélső'), ('ST', 'Csatár'), ('CF', 'Középcsatár')], max_length=3),
        ),
    ]
