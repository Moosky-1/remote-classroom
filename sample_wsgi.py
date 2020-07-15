# This file contains the WSGI configuration required to serve up your
# web application at http://Moosky.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#

# +++++++++++ GENERAL DEBUGGING TIPS +++++++++++
# getting imports and sys.path right can be fiddly!
# We've tried to collect some general tips here:
# https://help.pythonanywhere.com/pages/DebuggingImportError



# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#Online Elearning Portal Python 3 and Django 3/

# assuming your django settings file is at '/home/Moosky/mysite/mysite/settings.py'
# and your manage.py is is at '/home/Moosky/mysite/manage.py'
path = '/home/pythonanywhere/projectname'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'projectname.settings'

# then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
