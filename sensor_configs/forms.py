from django import forms
import json


class ConfigForm(forms.Form):

    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, json_config, db_config=None, *args, **kwargs, ):
        super(ConfigForm, self).__init__(*args, **kwargs)
        with open(f"templates/configs/{json_config}") as f:
            sensor_config = json.load(f)
        if db_config:
            for field, settings in sensor_config.items():
                settings["kwargs"]["initial"] = db_config[field]
                if settings["model"] == "BooleanField":
                    self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                           required=False, widget=forms.CheckboxInput)
                elif settings["model"] == "MultipleChoiceField":
                    self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                           widget=forms.CheckboxSelectMultiple)
                else:
                    self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"])

        else:
            for field, settings in sensor_config.items():
                if settings["model"] == "BooleanField":
                    self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                           required=False, widget=forms.CheckboxInput)
                elif settings["model"] == "MultipleChoiceField":
                    self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                           widget=forms.CheckboxSelectMultiple)
                else:
                    self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"])