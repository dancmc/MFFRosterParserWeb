import sys
sys.path.insert(0, '/var/www/app_dancmc/mff')
sys.path.insert(0, '/var/www/app_dancmc')

# logging code should go here

# from app import app as application

from werkzeug.wsgi import DispatcherMiddleware
from mff.app import app as app_mff

# if __name__.startswith('_mod_wsgi_'):
#    multiprocessing.freeze_support()

application = DispatcherMiddleware(app_mff,{
})