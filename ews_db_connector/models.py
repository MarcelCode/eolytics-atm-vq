# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.gis.db import models


class EwsProject(models.Model):
    region = models.CharField(max_length=40)
    sensor = models.ForeignKey('Sensor', models.DO_NOTHING, db_column='sensor')
    pc_hostname = models.CharField(max_length=30)
    product = models.ForeignKey('Product', models.DO_NOTHING, db_column='product')
    project = models.ForeignKey('Project', models.DO_NOTHING, db_column='project')
    project_template = models.ForeignKey('ProjectTemplate', models.DO_NOTHING, db_column='project_template', blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    ews_name = models.CharField(unique=True, max_length=8)
    water_type = models.ForeignKey('WaterType', models.DO_NOTHING, db_column='water_type', blank=True, null=True)
    project_xml = models.OneToOneField('ProjectXml', models.DO_NOTHING, db_column='project_xml', blank=True, null=True)
    imagepart = models.ForeignKey('Imagepart', models.DO_NOTHING, db_column='imagepart', blank=True, null=True)
    user_id = models.IntegerField()
    user_project_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'ews_project'


class Ignore(models.Model):
    ident = models.CharField(max_length=255)
    ews_project = models.ForeignKey(EwsProject, models.DO_NOTHING, db_column='ews_project')

    class Meta:
        managed = False
        db_table = 'ignore'
        unique_together = (('ident', 'ews_project'),)


class Imagepart(models.Model):
    ul_lon = models.FloatField()
    ul_lat = models.FloatField()
    lr_lon = models.FloatField()
    lr_lat = models.FloatField()

    class Meta:
        managed = False
        db_table = 'imagepart'
        unique_together = (('ul_lon', 'ul_lat', 'lr_lon', 'lr_lat'),)


class Job(models.Model):
    mission = models.IntegerField(blank=True, null=True)
    jobfile = models.IntegerField(blank=True, null=True)
    qflag_cfg = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    stop_time = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    stop_action = models.CharField(max_length=500, blank=True, null=True)
    start_action = models.CharField(max_length=500, blank=True, null=True)
    waterglob_cfg = models.IntegerField(blank=True, null=True)
    waterdetect_cfg = models.IntegerField(blank=True, null=True)
    wstaubig_cfg = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job'


class LogAdm(models.Model):
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    ews_project = models.IntegerField(blank=True, null=True)
    modul = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_adm'


class LogMissions(models.Model):
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    mission = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    modul = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_missions'


class LogServer(models.Model):
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    level = models.CharField(max_length=50, blank=True, null=True)
    ews_project = models.IntegerField(blank=True, null=True)
    modul = models.CharField(max_length=50, blank=True, null=True)
    function = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'log_server'


class Mission(models.Model):
    projectxml = models.CharField(max_length=255)
    ident = models.CharField(max_length=255)
    year = models.IntegerField()
    jd = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    actiondatetime = models.DateTimeField(blank=True, null=True)
    actiondescription = models.CharField(max_length=255, blank=True, null=True)
    actionname = models.CharField(max_length=255, blank=True, null=True)
    activeaction = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    ews_project = models.ForeignKey(EwsProject, models.DO_NOTHING, db_column='ews_project')

    class Meta:
        managed = False
        db_table = 'mission'
        unique_together = (('ident', 'ews_project'),)


class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=3)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class Project(models.Model):
    project_name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'project'

    def __str__(self):
        return self.project_name


class ProjectTemplate(models.Model):
    template_name = models.CharField(unique=True, max_length=40)

    class Meta:
        managed = False
        db_table = 'project_template'


class ProjectXml(models.Model):
    sourcedir = models.CharField(max_length=200)
    importdir = models.CharField(max_length=200)
    exportdir = models.CharField(max_length=200)
    bindir = models.CharField(max_length=200)
    dimapdir = models.CharField(max_length=200)
    missionrootdir = models.CharField(max_length=200)
    rootdir = models.CharField(max_length=200)
    defaultmissiondir = models.CharField(max_length=200)
    serverport = models.IntegerField()
    servermode_auto = models.CharField(max_length=10, blank=True, null=True)
    jobmode_foreground = models.CharField(max_length=10, blank=True, null=True)
    jobmode_autoexit = models.CharField(max_length=10, blank=True, null=True)
    cpus = models.IntegerField(blank=True, null=True)
    sourcecheckintervall = models.IntegerField()
    orderdelay = models.IntegerField()
    queuedir = models.CharField(max_length=200)
    ignoreorderdir = models.CharField(max_length=200)
    colorpalettegray = models.CharField(max_length=200)
    colorpalettecolor = models.CharField(max_length=200)
    colorpaletteflag = models.CharField(max_length=200, blank=True, null=True)
    colorpalettediff = models.CharField(max_length=200, blank=True, null=True)
    gain = models.IntegerField(blank=True, null=True)
    colorpalettetsm = models.CharField(max_length=200, blank=True, null=True)
    colorpalettephy = models.CharField(max_length=200, blank=True, null=True)
    colorpalettecdm = models.CharField(max_length=200, blank=True, null=True)
    colorpalettequc = models.CharField(max_length=200, blank=True, null=True)
    colorpalettequt = models.CharField(max_length=200, blank=True, null=True)
    colorpalettez90 = models.CharField(max_length=200, blank=True, null=True)
    jobmode_cleanup = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_xml'


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=40)
    resolution = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sensor'
        unique_together = (('sensor_name', 'resolution'),)


class Sources(models.Model):
    filename = models.CharField(max_length=255)
    mission = models.ForeignKey(Mission, models.DO_NOTHING, db_column='mission')

    class Meta:
        managed = False
        db_table = 'sources'


class WaterType(models.Model):
    type = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'water_type'
