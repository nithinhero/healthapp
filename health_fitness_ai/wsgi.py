import os
from dotenv import load_dotenv  # ✅ ADD THIS
from django.core.wsgi import get_wsgi_application

# ✅ Load environment variables before Django setup
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_fitness_ai.settings')

from django.core.management import call_command
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print("Auto migration failed:", e)

application = get_wsgi_application()
