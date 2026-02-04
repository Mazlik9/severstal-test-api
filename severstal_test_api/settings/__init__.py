import os

environment = os.getenv('ENVIRONMENT', 'local')

if environment == 'production':
    from .production import *
elif environment == 'development':
    from .development import *
else:  # local
    from .local import *