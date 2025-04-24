import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_fitness_ai.settings')

application = get_wsgi_application()
