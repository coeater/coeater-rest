# Generated by Django 3.1.2 on 2020-10-14 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20201014_1446'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitation',
            old_name='target',
            new_name='invitee',
        ),
        migrations.RenameField(
            model_name='invitation',
            old_name='owner',
            new_name='inviter',
        ),
    ]