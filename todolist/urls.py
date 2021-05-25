from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns=[
    path("login",views.onlogin,name="login"),
    path("addtask",views.addtask,name="addtask"),
    path("deltask",views.deltask,name="deltask"),
    path("delete",views.delete,name="delete"),
    path("sendmsg",views.sendmsg,name="sendmsg"),
]