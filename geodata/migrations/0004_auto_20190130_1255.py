# Generated by Django 2.1.4 on 2019-01-30 11:55

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0003_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]
