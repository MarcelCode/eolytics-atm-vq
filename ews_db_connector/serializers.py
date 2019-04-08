from rest_framework import serializers
from projects.models import UserProject
from .models import Mission
import datetime


class UserProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProject
        fields = ("watertype", "ews_name", "region", "state_new")


class MissionSerializer(serializers.ModelSerializer):
    actiondatetime_local = serializers.SerializerMethodField()

    def get_actiondatetime_local(self, obj):
        local_time = int(self.context['request'].COOKIES['local_time'])
        local_time *= -1
        local_time = obj.actiondatetime + datetime.timedelta(minutes=local_time)
        return local_time

    class Meta:
        model = Mission
        fields = ("ident", "get_scene_datetime", "state", "status_percentage", "actiondescription",
                  "time_elapsed", "actiondatetime_local", "pk")
