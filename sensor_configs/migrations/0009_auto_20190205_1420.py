# Generated by Django 2.1.4 on 2019-02-05 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0009_auto_20190205_1307'),
        ('sensor_configs', '0008_auto_20190205_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='imgpart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imgpart', to='geodata.UserProjectShape'),
        ),
        migrations.AddField(
            model_name='config',
            name='mask_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mask_image', to='geodata.UserProjectShape'),
        ),
        migrations.AddField(
            model_name='config',
            name='polygonstatistics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polygonstatistics', to='geodata.UserProjectShape'),
        ),
    ]
