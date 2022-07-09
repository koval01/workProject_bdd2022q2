#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imgcollector.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    exclude_flags = ["debug", "docker_test"]
    args = sys.argv
    for flag in exclude_flags:
        sys.argv.append(sys.argv.pop(sys.argv.index(flag))) \
            if flag in sys.argv else None
        args = sys.argv[:-1] if flag in sys.argv else args

    execute_from_command_line(args)


if __name__ == '__main__':
    main()
