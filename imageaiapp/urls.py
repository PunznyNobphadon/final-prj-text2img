from django.urls import path
from imageaiapp.views import *

urlpatterns = [
    path("",home),
    path("imageai/",imageai),
    #path("logins/",logins),
    #path('logout/', logout),
    #path('registes/', registers),
    #path("",),
]

