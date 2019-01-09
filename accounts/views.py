from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from portal.models import Sensor
from django.contrib.auth import logout

User = get_user_model()


def login_user(request, authentication_form=AuthenticationForm):
    next = request.GET.get("next", None)
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect("projects")
        else:
            form = authentication_form(data=request.POST)
    else:
        if request.user.is_authenticated:
            return redirect("projects")

        form = authentication_form(request)

    return TemplateResponse(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)

    return redirect("login")
