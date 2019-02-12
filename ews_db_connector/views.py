from rest_framework.views import APIView
from rest_framework.response import Response


class HelloView(APIView):

    def get(self, request, project_pk):
        content = {'project_pk': project_pk}
        return Response(content)

