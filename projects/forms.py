from django import forms
from projects.models import UserProject, UserSensor
from ews_db_connector.models import EwsProject, Mission
from crispy_forms.layout import Field
from projects.tools import get_available_cores
import json


def create_core_choices(cores):
    cores += 1
    choices = [(x, x) for x in range(cores)]
    return choices


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        exclude = ("user", "ews_name", "state", "automatic_mode", "cores")

    def __init__(self, user, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['sensor'].queryset = UserSensor.objects.get(user=user).sensors
        self.fields["project_abbrevation"].widget.attrs["pattern"] = ".{3,}"
        self.fields["project_abbrevation"].help_text = "Has to be 3 characters long."


class FinalDownloadForm(forms.Form):

    def __init__(self, project_pk, *args, **kwargs):
        super(FinalDownloadForm, self).__init__(*args, **kwargs)
        user_project = UserProject.objects.get(pk=project_pk)
        ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
        final_downloads = Mission.objects.filter(ews_project=ews_project, state="finished")
        self.fields['missions'].queryset = final_downloads
