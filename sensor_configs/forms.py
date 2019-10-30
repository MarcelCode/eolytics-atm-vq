from django import forms
from geodata.models import UserProjectShape
import json
from sensor_configs.tools import config_initial
import numexpr as ne
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ConfigForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, json_config, db_config=None, *args, **kwargs, ):
        super(ConfigForm, self).__init__(*args, **kwargs)
        with open(f"templates/configs/{json_config}") as f:
            sensor_config = json.load(f)
        if db_config:
            for field, settings in sensor_config.items():
                if field in db_config:
                    settings["kwargs"]["initial"] = db_config[field]
                self.create_fields(field, settings)
        else:
            for field, settings in sensor_config.items():
                self.create_fields(field, settings)

    def create_fields(self, field, settings):
        if settings["model"] == "BooleanField":
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                   required=False, widget=forms.CheckboxInput)
        elif settings["model"] == "MultipleChoiceField":
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                   widget=forms.CheckboxSelectMultiple)
        elif "step" in settings:
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                   widget=forms.NumberInput(
                                                                       attrs={"step": settings["step"]}
                                                                   ))
        else:
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"])

        if "seperator" in settings:
            self.fields[field].widget.attrs['class'] = 'seperator'


class ConfigShapeForm(forms.Form):
    def __init__(self, user_project, config, *args, **kwargs):
        super(ConfigShapeForm, self).__init__(*args, **kwargs)
        shapes = UserProjectShape.objects.filter(user_project=user_project)
        if shapes.exists():
            choices = list(shapes.values_list("pk", "name"))
            choices.insert(0, (None, "-------"))
        else:
            choices = [(None, "-------")]

        self.fields['aoi'] = forms.ChoiceField(choices=choices, label="Area of Interest",
                                               initial=config_initial(config.imgpart),
                                               required=False,
                                               help_text="Process only a pre-defined area of interest (AOI)")


class MaskingForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, json_mask, db_config=None, *args, **kwargs, ):
        super(MaskingForm, self).__init__(*args, **kwargs)
        with open(f"templates/mask_definition/{json_mask}") as f:
            sensor_config = json.load(f)
        if db_config:
            for field, settings in sensor_config.items():
                if field in db_config:
                    settings["kwargs"]["initial"] = db_config[field]
                self.create_fields(field, settings)

        else:
            for field, settings in sensor_config.items():
                self.create_fields(field, settings)

    def create_fields(self, field, settings):
        if settings["model"] == "BooleanField":
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                   required=False, widget=forms.CheckboxInput)
        elif settings["model"] == "MultipleChoiceField":
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                   widget=forms.CheckboxSelectMultiple)
        elif "step" in settings:
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"],
                                                                   widget=forms.NumberInput(
                                                                       attrs={"step": settings["step"]}
                                                                   ))
        else:
            self.fields[field] = getattr(forms, settings["model"])(label=settings["name"], **settings["kwargs"])

        if "seperator" in settings:
            self.fields[field].widget.attrs['class'] = 'seperator'


class UploadShapeForm(forms.Form):
    name = forms.CharField(max_length=100)
    file = forms.FileField(help_text="Only zipped ESRI shapefiles allowed (*.zip).")

    def __init__(self, *args, **kwargs):
        super(UploadShapeForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs['accept'] = '.zip, .rar, .7z'
