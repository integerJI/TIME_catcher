# Generated by Django 2.1.8 on 2020-07-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeUser', '0006_remove_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='plan',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
