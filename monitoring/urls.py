from django.contrib import admin
from django.urls import include, path
from . import views
from . import auth0backend
from social_django import views as social_django_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('pedidos/', include('pedidos.urls')),       
    path('operarios/', include('operarios.urls')),   

    # Rutas de autenticación
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
    path('login/auth0', social_django_views.auth, {'backend': 'auth0'}, name='login'),]


