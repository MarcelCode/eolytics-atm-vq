from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import UserProject
from .models import Mission
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from ews_db_connector.serializers import UserProjectSerializer, MissionSerializer
from ews_db_connector.ews_requests import EwsUserQueries
from rest_framework.exceptions import PermissionDenied


class UserProjectView(ListAPIView):
    serializer_class = UserProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return UserProject.objects.filter(user=user)


class ProjectMissionsView(ListAPIView):
    serializer_class = MissionSerializer

    def get_queryset(self):
        ews_project = UserProject.objects.get(pk=self.kwargs['project_pk'])
        if self.request.user == ews_project.user:
            ews_missions = EwsUserQueries().get_missions(ews_project.ews_name)
            return ews_missions
        raise PermissionDenied({"message": "You don't have permission to access"})
