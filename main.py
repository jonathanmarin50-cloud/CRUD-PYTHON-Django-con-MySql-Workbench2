import os
import django
from django.core.asgi import get_asgi_application

# Configuración del entorno de Django: Apuntamos a los ajustes de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Inicializamos Django (necesario para que las apps se carguen correctamente)
django.setup()

# Exportamos la aplicación como 'app'. 
# Esto es lo que busca el comando 'uvicorn main:app'
app = get_asgi_application()
