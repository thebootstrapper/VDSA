# Generated by Django 2.1.3 on 2019-01-17 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backoffice', '0005_delete_myfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='nom',
        ),
    ]
