#!/usr/bin/env python
import os
import sys

sys.path.append('/home/phonese/lib')
sys.path.append('/home/jason/sites/q.zzq.org')

os.environ['DJANGO_SETTINGS_MODULE'] = 'q.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
