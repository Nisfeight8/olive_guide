# Generated by Django 3.2.8 on 2021-11-07 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olive_grove', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='olivegrove',
            name='srid',
        ),
    ]
