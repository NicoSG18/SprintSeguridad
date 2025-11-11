"""
Django settings for monitoring project.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'svm_)tpa-o^gkn@81sel&lapq2jc7^^-n9c+4y&f9rymz$kum_'
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- CAMBIO 1: Tus Apps de Provesi ---
    # Se quitan las apps del laboratorio
    # 'measurements',
    # 'variables',
    
    # Se añaden tus apps nuevas
    'pedidos',
    'operarios',
    
    # Se añade la app de Auth0
    'social_django', 
    # ------------------------------------
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
# Esta configuración es PERFECTA para el Terraform original.
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'monitoring_db',
         'USER': 'monitoring_user',
         'PASSWORD': 'isis2503',
         'HOST': os.getenv('DATABASE_HOST', 'localhost'), # Terraform pasa esta variable
         'PORT': '5432', # Asegúrate de que el original usa 5432, no ''
     }
}


# Password validation
# ... (Sin cambios) ...
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
# ... (Sin cambios) ...
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# ... (Sin cambios) ...
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static', 'media')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# ----------------------------------------------------------------------
# 🔑 CAMBIO 2: Añadir la Configuración de Auth0 (del laboratorio)
# ----------------------------------------------------------------------

LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/"
# (Usamos os.getenv para la IP pública que Terraform nos dará)
EXTERNAL_URL = f"http://{os.getenv('PUBLIC_IP', 'localhost:8080')}"
LOGOUT_REDIRECT_URL = f"https_://dev-wd5yikr0h44ic7hv.us.auth0.com/v2/logout?returnTo={EXTERNAL_URL}" 

SOCIAL_AUTH_TRAILING_SLASH = False 
SOCIAL_AUTH_AUTH0_DOMAIN = 'dev-wd5yikr0h44ic7hv.us.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'xabDTb3giiyO8KUm9nvzNPiIpD45d4st'
SOCIAL_AUTH_AUTH0_SECRET = '1i52o7ZBuaW7AOkCgR_cMOZzQZtp7W3MX8TTZvd3qwk1kHYBEvSgJQMMh4Cof5W' # (Esta es tu secret key)

SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email',
    'role', # <-- Importante: Pide el rol
]

AUTHENTICATION_BACKENDS = {
    'monitoring.auth0backend.Auth0', # (Asegúrate que este archivo existe)
    'django.contrib.auth.backends.ModelBackend',
}