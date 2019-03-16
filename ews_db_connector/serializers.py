from rest_framework import serializers
from projects.models import UserProject
from .models import Mission


class UserProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProject
        fields = ("watertype", "ews_name", "region", "state_new")


class MissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mission
        fields = ("ident", "get_scene_datetime", "state", "status_percentage", "actiondescription",
                  "time_elapsed", "actiondatetime", "pk")
