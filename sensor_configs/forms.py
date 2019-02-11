from django import forms
from geodata.models import UserProjectShape
import json
from sensor_configs.tools import config_initial
from django.forms.widgets import NumberInput


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


class ConfigShapeForm(forms.Form):
    def __init__(self, user_project, config, *args, **kwargs):
        super(ConfigShapeForm, self).__init__(*args, **kwargs)
        shapes = UserProjectShape.objects.filter(user_project=user_project)
        if shapes.exists():
            choices = list(shapes.values_list("pk", "name"))
            choices.insert(0, (None, "-------"))
        else:
            choices = [(None, "-------")]

        self.fields['imgpart'] = forms.ChoiceField(choices=choices, label="Process AOI",
                                                   initial=config_initial(config.imgpart),
                                                   required=False,
                                                   help_text="Process only a pre-defined area of interest (AOI)")

        self.fields['mask_image'] = forms.ChoiceField(choices=choices, label="Mask out regions outside AOI",
                                                      initial=config_initial(config.mask_image), required=False,
                                                      help_text="Mask out regions that shall not be processed by"
                                                                " defining a precise area of interest, e.g. the"
                                                                " exact water body you are interested in.")

        self.fields['polygonstatistics'] = forms.ChoiceField(choices=choices, label="Run Polygonstatistics",
                                                             initial=config_initial(config.polygonstatistics),
                                                             required=False,
                                                             help_text="Calculate statistics within specific"
                                                                       " regions, defined as single features within"
                                                                       " an ESRI Shapefile.")

        self.fields['static_mask'] = forms.ChoiceField(choices=choices, label="Static Mask",
                                                       initial=config_initial(config.static_mask),
                                                       required=False,
                                                       help_text="Use static shapes for product masking,"
                                                                 " e.g. shallow water areas.")


class MaskingForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, required=False)

    def __init__(self, db_config=None, *args, **kwargs, ):
        super(MaskingForm, self).__init__(*args, **kwargs)
        with open(f"templates/mask_definition/mask_definitions.json") as f:
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


class UploadShapeForm(forms.Form):
    name = forms.CharField(max_length=100)
    file = forms.FileField(help_text="Only zipped ESRI shapefiles allowed (*.zip).")

    def __init__(self, *args, **kwargs):
        super(UploadShapeForm, self).__init__(*args, **kwargs)
        self.fields["file"].widget.attrs['accept'] = '.zip, .rar, .7z'
