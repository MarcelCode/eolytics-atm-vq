from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import UserProject
from .models import Mission
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from ews_db_connector.serializers import UserProjectSerializer


class UserProjectView(ListAPIView):
    serializer_class = UserProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return UserProject.objects.filter(user=user)


