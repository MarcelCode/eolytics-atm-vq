# Generated by Django 2.1.4 on 2019-01-30 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GeoDataLandsat8',
        ),
        migrations.DeleteModel(
            name='GeoDataSentinel2',
        ),
        migrations.DeleteModel(
            name='GeoDataSentinel3',
        ),
    ]
