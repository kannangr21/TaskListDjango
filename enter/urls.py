from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns=[
    path("login",views.login,name="login"),
    path("reset",views.reset,name="reset"),
    path("regsub",views.regsub,name="regsub"),
    path("reverify",views.reverify,name="reverify"),
    path("passverify",views.passverify,name="passverify"),
    path("verify",views.verify,name="verify"),
    path("logout",views.logout,name="logout"),
]