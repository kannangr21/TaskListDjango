from django.contrib import admin

# Register your models here.
from .models import Tasks,temp
admin.site.register(temp)
admin.site.register(Tasks)
