import pytest

@pytest.fixture(autouse=True)
def fast_password_hasher(settings):
    settings.PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

@pytest.fixture(autouse=True)
def disable_migrations(settings):
    class DisableMigrations:
        def __contains__(self, item): return True
        def __getitem__(self, item): return None
    settings.MIGRATION_MODULES = DisableMigrations()

@pytest.fixture(autouse=True)
def use_sqlite_memory(settings):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'ATOMIC_REQUESTS': False,  # 👈 evita el KeyError
    }
