# Generated by Django 2.1.4 on 2019-01-28 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensor_configs', '0004_auto_20190126_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='ews_ident',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
