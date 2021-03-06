from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from sensor_configs.models import Sensor
from django.contrib.auth import logout
from datetime import datetime
from django.contrib import messages
import pytz
from accounts.models import Profile

User = get_user_model()


def check_licence_duration(request, user):
    licence_end_date = Profile.objects.get(user=user).temporal_licence
    if licence_end_date:
        utc_now = datetime.now().date()
        if utc_now <= licence_end_date:
            return True
        else:
            messages.error(request, 'Your licence agreement is outdated. Please contact us.')
            return False
    else:
        return True


def login_user(request, authentication_form=AuthenticationForm):
    next = request.GET.get("next", None)
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and check_licence_duration(request, user):
            login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect("/projects/all")
        else:
            form = authentication_form(data=request.POST)
    else:
        if request.user.is_authenticated:
            return redirect("/projects/all")

        form = authentication_form(request)

    return TemplateResponse(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)

    return redirect("login")
