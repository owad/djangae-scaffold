#!/usr/bin/env python
import os
import sys

from {{ project_name }}.boot import fix_path
fix_path(include_dev_libs_path='test' in sys.argv)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{ project_name }}.settings")

    from djangae.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
