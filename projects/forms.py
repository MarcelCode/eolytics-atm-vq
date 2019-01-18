from django import forms
from .models import UserSensor, Watertype, UserProject

GROUND_LEVEL_CHOICES = ([0, "0"], [400, "400"], [1000, "1000"], [1900, "1900"])


def sensor_choices(user):
    user_sensors = UserSensor.objects.get(user=user)
    user_sensor_objects = user_sensors.sensors.all()
    choices = list(zip(user_sensor_objects, user_sensor_objects.values_list("sensor", flat=True)))
    return choices


def watertype_choices():
    watertype_objects = Watertype.objects.all()
    choices = list(zip(watertype_objects, watertype_objects.values_list("name", flat=True)))
    return choices


class CreateProjectForm(forms.ModelForm):
    ground_level_over_sea = forms.ChoiceField(choices=GROUND_LEVEL_CHOICES)

    class Meta:
        model = UserProject
        exclude = ("user", "ews_unique_project_name")

    def __init__(self, user, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['sensor'].queryset = UserSensor.objects.get(user=user).sensors

