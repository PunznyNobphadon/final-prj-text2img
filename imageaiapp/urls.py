from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('imageai/',views.imageai, name='imageai'),
    path('login/',views.logins, name='logins'),
    path('logout/', views.logout, name='logout'),
    path('registes/',views.registers, name='registes'),
    path('sign-in', views.sign_in, name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    #path('generate/', views.generate_image, name='generate'),
]

