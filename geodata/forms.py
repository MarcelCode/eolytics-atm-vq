from django import forms
from portal import models
import inspect
import sys


# Forms need the same name like the geodata models
class Landsat8(forms.ModelForm):
    product_list = forms.ModelMultipleChoiceField(models.Products.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple, initial=models.all_products)

    rrs_config = forms.ModelMultipleChoiceField(models.RrsConfig.objects.all(),
                                                widget=forms.CheckboxSelectMultiple, initial=models.all_rrs_config)

    project_name = forms.CharField(max_length=200, required=True)

    class Meta:
        model = models.Landsat8
        exclude = ["user", "default_config"]


class Sentinel2(forms.ModelForm):
    product_list = forms.ModelMultipleChoiceField(models.Products.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple, initial=models.all_products)

    rrs_config = forms.ModelMultipleChoiceField(models.RrsConfig.objects.all(),
                                                widget=forms.CheckboxSelectMultiple, initial=models.all_rrs_config)

    project_name = forms.CharField(max_length=200, required=True)

    class Meta:
        model = models.Sentinel2
        exclude = ["user", "default_config"]


def get_form_objects():
    classes = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            classes[name] = obj

    return classes
