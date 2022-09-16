from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('check_name/', views.check_name),
    path('login/', views.login),
]
