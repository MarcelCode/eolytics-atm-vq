# Generated by Django 2.1.4 on 2019-02-07 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20190125_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproject',
            name='cores',
            field=models.IntegerField(default=0),
        ),
    ]
