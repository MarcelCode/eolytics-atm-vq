# Generated by Django 2.1.4 on 2019-01-02 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0002_sentinel2_sentinel3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentinel2',
            name='path',
        ),
        migrations.RemoveField(
            model_name='sentinel2',
            name='row',
        ),
        migrations.RemoveField(
            model_name='sentinel2',
            name='sequence',
        ),
        migrations.AddField(
            model_name='sentinel2',
            name='name',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]