from django.contrib import admin
from django.urls import path
from django.urls import include
from django.urls import re_path as url
from myapp import urls as UserUrl

urlpatterns = [
    url(r"", include(UserUrl)),
]
