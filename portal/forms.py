from django import forms
from portal import models
from django.forms.widgets import CheckboxSelectMultiple


class OrderForm(forms.ModelForm):
    product_list = forms.ModelMultipleChoiceField(models.Products.objects.all(),
                                                  widget=forms.CheckboxSelectMultiple, initial=models.all_products)

    rrs_config = forms.ModelMultipleChoiceField(models.RrsConfig.objects.all(),
                                                widget=forms.CheckboxSelectMultiple, initial=models.all_rrs_config)

    class Meta:
        model = models.DefaultSettings
        exclude = ["user", "satellite"]
