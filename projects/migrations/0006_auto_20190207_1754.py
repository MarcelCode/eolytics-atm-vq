# Generated by Django 2.1.4 on 2019-02-07 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_userproject_cores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproject',
            name='cores',
            field=models.IntegerField(default=6),
        ),
    ]
