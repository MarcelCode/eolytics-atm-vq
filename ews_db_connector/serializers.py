from rest_framework import serializers
from .models import Mission


class MissionSerializer(serializers.ModelSerializer):
    created_date = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    def get_created_date(self, obj):
        return f'{obj.year}-{obj.month}-{obj.day}'

    def get_created_time(self, obj):
        return f'{obj.hour}:{obj.minute}'

    class Meta:
        model = Mission
        fields = ('created_date', 'created_time', 'state', "activeaction", "actionname", "actiondescription",
                  "actiondatetime")
