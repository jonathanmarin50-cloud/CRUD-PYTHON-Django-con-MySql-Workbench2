"""
Configuraciones globales del proyecto (Django Settings).
Este es el 'cerebro' del sistema. Aquí controlamos la base de datos, 
las aplicaciones instaladas y el idioma del sitio.
"""

from pathlib import Path
import os

# Intentar cargar variables de entorno de forma segura
try:
    from dotenv import load_dotenv
    import dj_database_url
    load_dotenv()
    HAS_ENV_LIBS = True
except ImportError:
    HAS_ENV_LIBS = False

# BASE_DIR: Indica la carpeta raíz donde está guardado todo tu proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY: Clave de seguridad única para este proyecto (No compartir en producción).
SECRET_KEY = 'django-insecure-pedidos-crud-secret-key-2024'

# DEBUG: Si es True, Django muestra errores detallados con fondo amarillo.
# Útil solo mientras estamos programando.
DEBUG = True

ALLOWED_HOSTS = ['*'] # Se recomienda ajustarlo luego a tu dominio de Render


# ============================================================
#  APLICACIONES INSTALADAS
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion',  # ⭐ Nuestra aplicación donde programamos el CRUD
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ⭐ Manejo eficiente de archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Buscamos las páginas HTML en la carpeta /templates/
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# ============================================================
#  CONEXIÓN A LA BASE DE DATOS (Supabase / Local)
# ============================================================
if HAS_ENV_LIBS:
    # Intentamos usar la URL completa (RECOMENDADO para Supabase/Producción)
    # Si no existe, usamos los parámetros individuales.
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

    # Si la configuración anterior falla (DATABASE_URL no definida), usamos el formato clásico
    if not DATABASES['default']:
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'bd_pedidos'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
else:
    # CONFIGURACIÓN DE EMERGENCIA / LOCAL (Si faltan librerías)
    # Usamos SQLite por defecto para evitar que el servidor se apague.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ============================================================
#  IDIOMA Y ZONA HORARIA
# ============================================================
LANGUAGE_CODE = 'es-co'         # Español de Colombia
TIME_ZONE = 'America/Bogota'    # Hora local de Bogotá
USE_I18N = True
USE_TZ = True


# ============================================================
#  ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # ⭐ Carpeta donde se recolectan los estáticos para producción

# Optimización de Whitenoise para mejorar el rendimiento
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
#  VALIDACIÓN DE CONTRASEÑAS (SEGURIDAD)
# ============================================================
# Estas reglas evitan que los usuarios creen contraseñas muy cortas o fáciles.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8, # Obliga a que la contraseña tenga al menos 8 caracteres.
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ============================================================
#  MENSAJES Y ALERTAS (BOOTSTRAP)
# ============================================================
# Mapeamos los mensajes de Django para que usen los colores de Bootstrap (success, danger, etc.)
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ============================================================
#  CONFIGURACIÓN DE SEGURIDAD (LOGIN)
# ============================================================
LOGIN_URL = '/cuentas/login/'              # Ruta exacta del login
LOGIN_REDIRECT_URL = 'dashboard'           # A dónde ir después de entrar
LOGOUT_REDIRECT_URL = '/cuentas/login/'    # A dónde ir al cerrar sesión

# ============================================================
#  CONFIGURACIÓN DE SESIONES (TIEMPO DE EXPIRACIÓN)
# ============================================================
# El tiempo se mide en segundos. 30 segundos = 30 segundos.
SESSION_COOKIE_AGE = 30

# Si se pone en True, la sesión se cierra al cerrar el navegador.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Si se pone en True, el tiempo de sesión se reinicia con cada clic que dé el usuario.
SESSION_SAVE_EVERY_REQUEST = True
