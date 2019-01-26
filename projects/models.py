from django.db import models
from django.contrib.auth import get_user_model
from sensor_configs.models import Sensor, Watertype


# Define which user is allowed to use which Sensors
class UserSensor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    sensors = models.ManyToManyField(Sensor)

    def __str__(self):
        return f"{self.user}"


class UserProject(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_project_name = models.CharField(max_length=100)
    project_abbrevation = models.CharField(max_length=3)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    watertype = models.ForeignKey(Watertype, on_delete=models.CASCADE)
    ews_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    state = models.CharField(max_length=20, blank=True, null=True)
    automatic_mode = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "user_project_name")

    def __str__(self):
        return f"{self.user},  {self.project_abbrevation}-{self.user_project_name}"

