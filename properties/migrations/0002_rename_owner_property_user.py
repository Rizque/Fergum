# Generated by Django 4.1.7 on 2023-04-01 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='owner',
            new_name='user',
        ),
    ]
