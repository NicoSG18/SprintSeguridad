"""
Django settings for monitoring project.
"""

import os
# Importar `Env` para leer variables de entorno de forma limpia
from environ import Env 

# Inicializar Env
env = Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --- Configuración de Variables de Entorno de Producción ---
# En producción (AWS), las variables se cargarán del archivo /etc/django_env
# creado por el script de Terraform. 
if os.path.exists('/etc/django_env'):
    # Cargar variables del archivo creado por Terraform
    env.read_env('/etc/django_env')
else:
    # Cargar variables de un archivo local .env_local si existe (para desarrollo)
    env.read_env(os.path.join(BASE_DIR, '.env_local'), override=True)


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
# ⚠️ Leer SECRET_KEY de la variable de entorno
SECRET_KEY = env('SECRET_KEY', default='svm_)tpa-o^gkn@81sel&lapq2jc7^^-n9c+4y&f9rymz$kum_')

# 🛑 CAMBIO CLAVE 1: Desactivar DEBUG para producción
DEBUG = env.bool('DEBUG', default=False) 

# 🌐 CAMBIO CLAVE 2: Leer ALLOWED_HOSTS de la variable de entorno o usar '*'
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 🎯 Aplicaciones de Provesi (Sustituyen a measurements y variables)
    'pedidos',      
    'operarios',    
    # 🔑 Librería Social Auth
    'social_django', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monitoring.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'monitoring', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monitoring.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# 🐘 CAMBIO CLAVE 3: Configuración de PostgreSQL leyendo variables de entorno
DATABASES = {
     'default': {
          'ENGINE': 'django.db.backends.postgresql', # Usamos 'postgresql' en lugar de 'postgresql_psycopg2'
          'NAME': env('DATABASE_NAME', default='monitoring_db'),
          'USER': env('DATABASE_USER', default='monitoring_user'),
          'PASSWORD': env('DATABASE_PASSWORD', default='isis2503'),
          # Usamos DATABASE_HOST que será la IP privada de la DB en AWS
          'HOST': env('DATABASE_HOST', default='localhost'), 
          'PORT': '5432',
     }
}


# Password validation
# ... (AUTH_PASSWORD_VALIDATORS are unchanged) ...


# Internationalization
# ... (LANGUAGE_CODE, TIME_ZONE, etc. are unchanged) ...


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# 📦 CAMBIO CLAVE 4: STATIC_ROOT fuera del código fuente, para Nginx
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_prod') 
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static', 'media')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# ----------------------------------------------------------------------
# 🔑 CONFIGURACIÓN DE AUTH0 (Integrada desde tus configuraciones anteriores)
# ----------------------------------------------------------------------

# --- RUTAS DE AUTENTICACIÓN ---
LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/"
# ⚠️ Usamos la variable EXTERNAL_URL (que contendrá la IP pública de AWS) para el logout.
EXTERNAL_URL = env('EXTERNAL_URL', default="http://localhost:8080")
LOGOUT_REDIRECT_URL = f"https://dev-wd5yikr0h44ic7hv.us.auth0.com/v2/logout?returnTo={EXTERNAL_URL}" 

# --- CREDENCIALES Y CONFIGURACIÓN DE AUTH0 ---
SOCIAL_AUTH_TRAILING_SLASH = False 
SOCIAL_AUTH_AUTH0_DOMAIN = 'dev-wd5yikr0h44ic7hv.us.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'xabDTb3giiyO8KUm9nvzNPiIpD45d4st'
SOCIAL_AUTH_AUTH0_SECRET = '1i52o7ZBuaW7AOkCgR_cMOZzQZtp7W3MX8TTZvd3qwk1kHYBEvSgJQMMh4Cof5W' # Reemplaza con tu Secret

# Solicitud de SCOPES
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email',
    'role', # <-- Pide el rol
]

# --- BACKENDS DE AUTENTICACIÓN ---
AUTHENTICATION_BACKENDS = {
    'monitoring.auth0backend.Auth0', 
    'django.contrib.auth.backends.ModelBackend',
}