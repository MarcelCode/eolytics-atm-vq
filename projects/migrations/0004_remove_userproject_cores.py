# Generated by Django 2.1.4 on 2019-02-07 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_userproject_cores'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userproject',
            name='cores',
        ),
    ]
