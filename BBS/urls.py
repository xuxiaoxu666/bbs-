from django.contrib import admin
from django.urls import path
from blog import views
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('check_name/', views.check_name),
    path('login/', views.login),
    path('get_code/', views.get_code),
    path('', views.index),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
