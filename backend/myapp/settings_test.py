from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "test-secret-key"
DEBUG = True

# ⚡ Solo las apps necesarias para tu proyecto y login
INSTALLED_APPS = [
    "django.contrib.auth",          # requerido por AbstractBaseUser y PermissionsMixin
    "django.contrib.contenttypes",  # requerido por el ORM
    "django.contrib.sessions",      # si usas login/session
    "myapp",                        # tu aplicación principal
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",  # 👈 necesario
    "django.middleware.common.CommonMiddleware",
]


ROOT_URLCONF = "myapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend" / "templates"],   # 👈 aquí deben estar tus templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "myapp.context_processors.user_context",
                "myapp.context_processors.carrito",
            ],
        },
    },
]

AUTH_USER_MODEL = 'myapp.Usuario'


WSGI_APPLICATION = "myapp.wsgi.application"

# ⚡ Base de datos en memoria para tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": False,
    }
}

# ⚡ Hasher rápido para tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# ⚡ Desactivar migraciones
class DisableMigrations:
    def __contains__(self, item): return True
    def __getitem__(self, item): return None

MIGRATION_MODULES = DisableMigrations()

# ⚡ Clave Stripe dummy para evitar errores en tests
STRIPE_SECRET_KEY = "sk_test_dummy"

# Idioma y zona horaria
LANGUAGE_CODE = "es-es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
