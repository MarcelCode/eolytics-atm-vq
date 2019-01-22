from ews_db_connector import serializers
from rest_framework.decorators import api_view
from projects.models import UserProject
from ews_db_connector.ews_requests import EwsUserQueries
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status


@login_required
@api_view(["GET"])
def missions_by_project(request, project_pk, format=None):
    try:
        ews_project = UserProject.objects.filter(user=request.user).get(pk=project_pk)
    except UserProject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    ews_missions = EwsUserQueries().get_missions(ews_project.ews_name)

    if request.method == 'GET':
        serializer = serializers.MissionSerializer(ews_missions, many=True)
        return Response(serializer.data)
