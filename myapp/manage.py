#!/usr/bin/env python
"""Script de administración de Django."""
import os
import sys


def main():
    """Ejecuta las tareas administrativas."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Verifica que el entorno virtual esté activo e instalado correctamente."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
