# Generated by Django 2.1.4 on 2019-01-25 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_project_name', models.CharField(max_length=100)),
                ('project_abbrevation', models.CharField(max_length=3)),
                ('ews_name', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('state', models.CharField(blank=True, max_length=20, null=True)),
                ('automatic_mode', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]