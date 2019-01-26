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


class ConfigForm(forms.Form):

    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, json_config, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        with open(f"templates/configs/{json_config}") as f:
            sensor_config = json.load(f)
        for field, settings in sensor_config.items():
            if not settings["model"] == "MultipleChoiceField":
                self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"])
            else:
                self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                       widget=forms.CheckboxSelectMultiple,
                                                                       initial=(c[0] for c in
                                                                                settings["kwargs"]["choices"]))

