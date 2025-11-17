"""
Django settings for mysite project.
"""

from pathlib import Path

# Base path
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-*uk%03&xyh&8gu5pb@cx51a&ez642)$%(hmipp%!u2b@1naveu'
DEBUG = True
ALLOWED_HOSTS = ["*"]   # Para desarrollo

# -----------------------------------------
# CORS + COOKIES + SESIONES (AJAX LOGIN)
# -----------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'myapp',
]

# settings.py
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "jhonh1540@gmail.com"
EMAIL_HOST_PASSWORD = "ufuh andz njge mspj"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER






AUTH_USER_MODEL = 'myapp.Usuario'


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # <── DEBE IR PRIMERO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Permitir credenciales (COOKIES) vía fetch()
CORS_ALLOW_CREDENTIALS = True

# Permitir cualquier origen en desarrollo
CORS_ALLOW_ALL_ORIGINS = True

# Cookies de sesión y CSRF en desarrollo
SESSION_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Necesario para evitar bloqueos con AJAX
CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'http://localhost:8000',
    'http://127.0.0.1',
    'http://127.0.0.1:8000',
]

# -----------------------------------------
# URLS
# -----------------------------------------

ROOT_URLCONF = 'mysite.urls'

LOGIN_REDIRECT_URL = 'catalogo'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'

# -----------------------------------------
# TEMPLATES
# -----------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Plantillas globales del frontend
        'DIRS': [BASE_DIR / "frontend" / "templates"],

        # Plantillas dentro de cada app
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "myapp.context_processors.user_context",  # 👈 aquí
            ],
        },
    },
]

# -----------------------------------------
# STATIC FILES
# -----------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "frontend" / "static",  # assets del frontend
    BASE_DIR / "static",               # estáticos globales
]

STATIC_ROOT = BASE_DIR / "staticfiles"

# -----------------------------------------
# MEDIA (Subidas del usuario)
# -----------------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------------------------
# BASE DE DATOS (MySQL)
# -----------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'codecommerce_db',
        'USER': 'root',
        'PASSWORD': 'Rickc137*',
        'HOST': '127.0.0.1', 
        'PORT': '3306',
        'OPTIONS': {
            'auth_plugin': 'mysql_native_password',
        }
    }
}

# -----------------------------------------
# PASSWORD VALIDATION
# -----------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------------------
# Django Settings globales
# -----------------------------------------

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
