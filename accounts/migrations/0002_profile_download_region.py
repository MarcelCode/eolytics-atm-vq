# Generated by Django 2.1.4 on 2019-01-30 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0005_auto_20190130_1301'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='download_region',
            field=models.ManyToManyField(to='geodata.Country'),
        ),
    ]