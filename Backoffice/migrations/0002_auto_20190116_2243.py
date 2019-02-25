# Generated by Django 2.1.5 on 2019-01-16 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backoffice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session_utilisateur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_s', models.CharField(max_length=100)),
                ('statut_s', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Statut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statuts', models.IntegerField(choices=[(1, 'Commercial'), (2, 'Magasin')], default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='admin',
            name='mdp',
            field=models.CharField(editable=False, max_length=64),
        ),
        migrations.AlterField(
            model_name='magasinvdsa',
            name='mdp_directeur',
            field=models.CharField(blank=True, editable=False, max_length=64, null=True),
        ),
    ]
