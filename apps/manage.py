#!/usr/bin/env python
#import os
import sys

import os,sys
virtenv = os.path.expanduser('') + '/home/morais/bethelenv/venv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
   if sys.version.split(' ')[0].split('.')[0] == '3':
       exec(compile(open(virtualenv, "rb").read(), virtualenv, 'exec'), dict(__file__=virtualenv))
   else:
       execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
   pass

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
