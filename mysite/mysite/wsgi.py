"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys
virtenv = os.path.expanduser('') + '/home/morais/work/bethelgroups/venv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
   if sys.version.split(' ')[0].split('.')[0] == '3':
       exec(compile(open(virtualenv, "rb").read(), virtualenv, 'exec'), dict(__file__=virtualenv))
   else:
       execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
   pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
