# Generated by Django 3.1.2 on 2020-11-07 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201030_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, upload_to='profiles'),
        ),
    ]
