from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from portal.models import Project

User = get_user_model()


def login_user(request, authentication_form=AuthenticationForm):
    next = request.GET.get("next", None)
    project_pk = Project.objects.first().pk
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect(f"/portal/{project_pk}")
        else:
            form = authentication_form(data=request.POST)
    else:
        if request.user.is_authenticated:
            return redirect(f"/portal/{project_pk}")

        form = authentication_form(request)

    return TemplateResponse(request, "accounts/login.html", {"form": form})
