from django.core.exceptions import PermissionDenied
from projects.models import UserProject


def owns_user_project(function):
    def wrap(request, *args, **kwargs):
        entry = UserProject.objects.get(pk=kwargs['project_pk'])
        if entry.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
