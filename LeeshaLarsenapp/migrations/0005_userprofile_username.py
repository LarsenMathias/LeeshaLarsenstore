# Generated by Django 4.1.3 on 2023-09-01 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeeshaLarsenapp', '0004_alter_userprofile_city_alter_userprofile_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]
