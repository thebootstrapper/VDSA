# Generated by Django 2.1.3 on 2019-01-17 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backoffice', '0002_auto_20190116_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=64)),
                ('source', models.FileField(upload_to='')),
            ],
        ),
    ]
