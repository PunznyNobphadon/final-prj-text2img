from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_image, name='generate_image'),
    path('display/<int:pk>/', views.display_image, name='display_image'),
    path('add/', views.add_image, name='add_image'),
    path('edit/<int:pk>/', views.edit_image, name='edit_image'),
    path('delete/<int:pk>/', views.delete_image, name='delete_image'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='image_generator/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='image_generator/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('about/',views.about,name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)