from django.contrib import admin
from django.urls import include, path
from . import views
from . import auth0backend

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('pedidos/', include('pedidos.urls')),       # <-- CAMBIO 3
    path('operarios/', include('operarios.urls')),   # <-- CAMBIO 4

    # Rutas de autenticación
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
    path('login/auth0', auth0backend.login, name='login'),
]


