# Generated by Django 2.1.8 on 2020-06-19 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeUser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='usr'),
        ),
    ]
