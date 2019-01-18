from django.db import models
from django.contrib.auth import get_user_model
from portal.models import Sensor


# Create your models here.
class UserSensor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    sensors = models.ManyToManyField(Sensor)

    def __str__(self):
        return f"{self.user.email}"


class Watertype(models.Model):
    ews_id = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ["ews_id"]

    def __str__(self):
        return f"{self.name}"


class UserProject(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    project_abbrevation = models.CharField(max_length=3)
    ground_level_over_sea = models.IntegerField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    watertype = models.ForeignKey(Watertype, on_delete=models.CASCADE)
    ews_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    state = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project_name")

    def __str__(self):
        return f"{self.user},  {self.project_abbrevation}-{self.project_name}"


