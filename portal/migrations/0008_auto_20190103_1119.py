# Generated by Django 2.1.4 on 2019-01-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0007_auto_20190103_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landsat8',
            name='config_name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='sentinel2',
            name='config_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]