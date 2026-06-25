import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_finder.settings')
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "team_finder.settings")
>>>>>>> 389f0e1d55554761fc530d18093297793c439f7d

application = get_asgi_application()
