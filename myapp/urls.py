from django.contrib import admin
from django.urls import re_path as url
from myapp.views import *



urlpatterns = [  
    #=========Session=================
    url(r'^$', index),
    url(r'^signup/$', signup),  
    url(r'^message/api/$', api),  
    url(r'^message/api/all/$', apimessage),  


]