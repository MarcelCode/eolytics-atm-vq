# Generated by Django 2.1.4 on 2019-07-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor_configs', '0012_auto_20190212_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='config_name',
            field=models.CharField(choices=[('landsat8.json', 'landsat8'), ('landsat5.json', 'landsat5'), ('sentinel2.json', 'sentinel2'), ('sentinel3.json', 'sentinel3')], max_length=255),
        ),
    ]
