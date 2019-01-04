from django.urls import path, re_path
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    path("", accounts_views.login_user, name='login'),
    path("accounts/login/", accounts_views.login_user, name="direct_login"),
    path("logout/", accounts_views.logout_view, name="logout")
    ]