from django.contrib import admin
from django.urls import include, path
from . import views
from . import auth0backend
from social_django import views as social_django_views # <-- AÑADIR ESTA LÍNEA

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('pedidos/', include('pedidos.urls')),       # <-- CAMBIO 3
    path('operarios/', include('operarios.urls')),   # <-- CAMBIO 4

    # Rutas de autenticación
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
    path('login/auth0', social_django_views.auth, {'backend': 'auth0'}, name='login'),]


