from django import forms
from projects.models import UserProject, UserSensor
from ews_db_connector.models import EwsProject, Mission
import json


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = UserProject
        exclude = ("user", "ews_name", "state", "automatic_mode")

    def __init__(self, user, *args, **kwargs):
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['sensor'].queryset = UserSensor.objects.get(user=user).sensors


class FinalDownloadForm(forms.Form):

    def __init__(self, project_pk, *args, **kwargs):
        super(FinalDownloadForm, self).__init__(*args, **kwargs)
        user_project = UserProject.objects.get(pk=project_pk)
        ews_project = EwsProject.objects.using("ews").get(ews_name=user_project.ews_name)
        final_downloads = Mission.objects.filter(ews_project=ews_project, state="finished")
        self.fields['missions'].queryset = final_downloads
