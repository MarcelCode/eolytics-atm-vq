from django.shortcuts import render
from map import models
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def home(request):
    if request.user.is_authenticated:
        return render(request, "portal/home.html")

    return redirect("login")