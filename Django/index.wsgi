import os
import sys

sys.path.append('/home/c/co31586/public_html/trest12/')
sys.path.append('/home/c/co31586/myenv/lib/python3.6/site-packages/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'trest12.settings'
import django
django.setup()

from django.core.handlers import wsgi
application = wsgi.WSGIHandler()
