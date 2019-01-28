from django import forms
from projects.models import UserProject, UserSensor
import json


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = UserProject
        exclude = ("user", "ews_name", "state", "automatic_mode")

    def __init__(self, user, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['sensor'].queryset = UserSensor.objects.get(user=user).sensors


