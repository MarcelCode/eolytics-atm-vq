from rest_framework import serializers
from projects.models import UserProject


class UserProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProject
        fields = ("watertype", "ews_name", "region", "state_new")
